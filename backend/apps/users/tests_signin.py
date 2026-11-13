"""
Signing in by emailed link: delivery, what the person is told, the other ways
in when there is no mail server, and the diagnosis of mail failures.
"""

import smtplib
import socket
import ssl
from io import StringIO

import pytest
from django.core import mail
from django.core.management import CommandError, call_command

from apps.users import tasks
from apps.users.emailing import diagnose
from apps.users.models import MagicLinkToken, User

REQUEST = "/api/v1/auth/magic-link/request/"
LOCMEM = "django.core.mail.backends.locmem.EmailBackend"
SMTP = "django.core.mail.backends.smtp.EmailBackend"


@pytest.fixture(autouse=True)
def fresh_rate_limit():
    """Sign-in requests are limited to 5 an hour per address; start each test clean."""
    from django.core.cache import cache

    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def mail_server(settings):
    """A configured mail server (messages land in django.core.mail.outbox)."""
    settings.EMAIL_BACKEND = LOCMEM
    settings.EMAIL_CONFIGURED = True
    settings.EMAIL_HOST = "mail.example.org"
    settings.MAGIC_LINK_LOG = False
    settings.FRONTEND_URL = "https://journal.example.org/"
    return settings


@pytest.fixture
def no_queue(monkeypatch):
    """The task queue is down: publishing a task fails immediately."""

    def refuse(*args, **kwargs):
        raise ConnectionError("broker unreachable")

    monkeypatch.setattr(tasks.send_magic_link_email, "apply_async", refuse)


@pytest.fixture
def queue_runs_inline(monkeypatch):
    """Stand in for a working queue: run the task right away."""

    def run(args=None, **kwargs):
        tasks.send_magic_link_email(*args)

    monkeypatch.setattr(tasks.send_magic_link_email, "apply_async", run)


def link_token(text: str) -> str:
    return text.split("/auth/verify?token=")[1].split()[0]


@pytest.mark.django_db
class TestEmailDelivery:
    def test_link_is_emailed_and_signs_the_person_in(
        self, api_client, user, mail_server, queue_runs_inline
    ):
        response = api_client.post(REQUEST, {"email": user.email})
        assert response.status_code == 200
        assert response.json()["delivery"] == "email"

        assert len(mail.outbox) == 1
        message = mail.outbox[0]
        assert message.to == [user.email]
        assert "https://journal.example.org/auth/verify?token=" in message.body
        assert "expires in 15 minutes" in message.body

        verified = api_client.post(
            "/api/v1/auth/magic-link/verify/", {"token": link_token(message.body)}
        )
        assert verified.status_code == 200 and "access_token" in verified.json()

    def test_address_is_matched_whatever_its_capitalisation(
        self, api_client, user, mail_server, queue_runs_inline
    ):
        api_client.post(REQUEST, {"email": user.email.upper()})
        assert len(mail.outbox) == 1

    def test_queue_down_still_delivers(self, api_client, user, mail_server, no_queue):
        response = api_client.post(REQUEST, {"email": user.email})
        assert response.status_code == 200
        assert len(mail.outbox) == 1  # sent from the request itself

    def test_unknown_address_gets_the_same_answer_and_no_account(
        self, api_client, user, mail_server, queue_runs_inline
    ):
        known = api_client.post(REQUEST, {"email": user.email}).json()
        unknown = api_client.post(REQUEST, {"email": "nobody@example.org"}).json()
        assert known == unknown
        assert len(mail.outbox) == 1
        assert not User.objects.filter(email="nobody@example.org").exists()

    def test_sign_up_by_email_when_the_operator_allows_it(
        self, api_client, mail_server, queue_runs_inline
    ):
        mail_server.ALLOW_EMAIL_SIGNUP = True
        response = api_client.post(REQUEST, {"email": "new.person@example.org"})
        assert response.status_code == 200
        assert User.objects.filter(email="new.person@example.org").exists()
        assert mail.outbox[0].to == ["new.person@example.org"]

    def test_deactivated_account_gets_nothing(
        self, api_client, user, mail_server, queue_runs_inline
    ):
        user.is_active = False
        user.save()
        assert api_client.post(REQUEST, {"email": user.email}).status_code == 200
        assert mail.outbox == []


@pytest.mark.django_db
class TestWithoutAMailServer:
    def test_link_goes_to_the_log_and_the_page_is_told_so(
        self, api_client, user, settings, queue_runs_inline, capsys
    ):
        settings.EMAIL_BACKEND = SMTP
        settings.EMAIL_CONFIGURED = False
        settings.MAGIC_LINK_LOG = True
        response = api_client.post(REQUEST, {"email": user.email})
        assert response.json()["delivery"] == "log"
        printed = capsys.readouterr().out
        assert "SIGN-IN LINK" in printed and "/auth/verify?token=" in printed
        # No attempt to reach a mail server that does not exist.
        assert mail.outbox == []

    def test_no_mail_and_no_log_is_an_honest_error_not_a_false_promise(
        self, api_client, user, settings
    ):
        settings.EMAIL_BACKEND = SMTP
        settings.EMAIL_CONFIGURED = False
        settings.MAGIC_LINK_LOG = False
        response = api_client.post(REQUEST, {"email": user.email})
        assert response.status_code == 503
        body = response.json()
        assert body["code"] == "SIGNIN_EMAIL_NOT_CONFIGURED"
        assert "signin_link" in body["suggestion"]
        assert MagicLinkToken.objects.count() == 0

    def test_methods_endpoint_describes_what_this_server_offers(
        self, api_client, settings
    ):
        settings.EMAIL_BACKEND = SMTP
        settings.EMAIL_CONFIGURED = True
        settings.GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_SECRET = ""
        settings.ALLOW_EMAIL_SIGNUP = False
        body = api_client.get("/api/v1/auth/methods/").json()
        assert body["email"] == {"delivery": "email"}
        assert body["google"] is False and body["signup"] is False

        settings.EMAIL_CONFIGURED = False
        settings.MAGIC_LINK_LOG = True
        settings.GOOGLE_CLIENT_ID, settings.GOOGLE_CLIENT_SECRET = "id", "secret"
        settings.ALLOW_EMAIL_SIGNUP = True
        body = api_client.get("/api/v1/auth/methods/").json()
        assert body["email"] == {"delivery": "log"}
        assert body["google"] is True and body["signup"] is True

        settings.MAGIC_LINK_LOG = False
        assert api_client.get("/api/v1/auth/methods/").json()["email"] == {
            "delivery": "unavailable"
        }

    def test_signin_link_command_makes_a_working_one_time_link(
        self, api_client, user, settings
    ):
        settings.FRONTEND_URL = "https://journal.example.org"
        out = StringIO()
        call_command("signin_link", user.email, stdout=out)
        token = link_token(out.getvalue())
        url = "/api/v1/auth/magic-link/verify/"
        assert api_client.post(url, {"token": token}).status_code == 200
        assert api_client.post(url, {"token": token}).status_code == 400  # once only

    def test_signin_link_command_can_create_the_account(self):
        with pytest.raises(CommandError, match="no account"):
            call_command("signin_link", "new@example.org", stdout=StringIO())
        out = StringIO()
        call_command(
            "signin_link", "new@example.org", "--create", "--name", "New", stdout=out
        )
        assert User.objects.get(email="new@example.org").display_name == "New"
        assert "/auth/verify?token=" in out.getvalue()


@pytest.mark.django_db
class TestFailures:
    def _broken(self, monkeypatch, exc):
        def fail(user, link):
            raise exc

        monkeypatch.setattr(tasks, "send_signin_email", fail)

    def test_failure_is_logged_with_its_cause_and_raised(
        self, user, mail_server, monkeypatch, caplog
    ):
        self._broken(
            monkeypatch, smtplib.SMTPAuthenticationError(535, b"bad credentials")
        )
        with pytest.raises(smtplib.SMTPAuthenticationError):
            tasks.deliver_signin_link(user, "tok")
        assert "MAIL_LOGIN_REJECTED" in caplog.text
        assert "EMAIL_HOST_PASSWORD" in caplog.text
        assert "tok" not in caplog.text  # the link itself is never logged here

    def test_failure_is_tolerated_when_the_link_is_in_the_log(
        self, user, mail_server, monkeypatch, capsys
    ):
        mail_server.MAGIC_LINK_LOG = True
        self._broken(monkeypatch, ConnectionRefusedError())
        tasks.deliver_signin_link(user, "tok")  # does not raise
        assert "/auth/verify?token=tok" in capsys.readouterr().out

    def test_request_still_answers_when_mail_and_queue_both_fail(
        self, api_client, user, mail_server, no_queue, monkeypatch
    ):
        self._broken(monkeypatch, TimeoutError())
        assert api_client.post(REQUEST, {"email": user.email}).status_code == 200

    @pytest.mark.parametrize(
        "exc,code,hint",
        [
            (
                smtplib.SMTPAuthenticationError(535, b"no"),
                "MAIL_LOGIN_REJECTED",
                "EMAIL_HOST_USER",
            ),
            (
                smtplib.SMTPRecipientsRefused({"a@b.c": (554, b"relay denied")}),
                "MAIL_RECIPIENT_REFUSED",
                "relay",
            ),
            (
                smtplib.SMTPSenderRefused(553, b"no", "x@y.z"),
                "MAIL_SENDER_REFUSED",
                "DEFAULT_FROM_EMAIL",
            ),
            (
                smtplib.SMTPHeloError(501, b"bad helo"),
                "MAIL_HELO_REJECTED",
                "MESH_HOSTNAME",
            ),
            (
                smtplib.SMTPNotSupportedError("STARTTLS extension not supported"),
                "MAIL_TLS_MISMATCH",
                "465",
            ),
            (
                ssl.SSLError("wrong version number"),
                "MAIL_TLS_MISMATCH",
                "EMAIL_USE_SSL",
            ),
            (
                smtplib.SMTPServerDisconnected("Connection unexpectedly closed"),
                "MAIL_TLS_MISMATCH",
                "587",
            ),
            (
                socket.gaierror("Name or service not known"),
                "MAIL_HOST_NOT_FOUND",
                "EMAIL_HOST",
            ),
            (ConnectionRefusedError(), "MAIL_CONNECTION_REFUSED", "localhost"),
            (TimeoutError(), "MAIL_TIMEOUT", "firewall"),
            (
                smtplib.SMTPDataError(552, b"mailbox full"),
                "MAIL_REJECTED",
                "mailbox full",
            ),
            (
                smtplib.SMTPDataError(550, b"5.7.1 Email rejected per DMARC policy."),
                "MAIL_SENDER_NOT_AUTHENTICATED",
                "EMAIL_HOST_USER",
            ),
            (OSError("Network is unreachable"), "MAIL_NETWORK_ERROR", "network"),
            (ValueError("odd"), "MAIL_FAILED", "send_test_email"),
        ],
    )
    def test_every_failure_has_a_cause_and_a_remedy(self, settings, exc, code, hint):
        settings.EMAIL_HOST, settings.EMAIL_PORT = "mail.example.org", 587
        problem = diagnose(exc)
        assert problem.code == code
        assert hint.lower() in str(problem).lower()
        assert problem.message and problem.suggestion


@pytest.mark.django_db
class TestSendTestEmailCommand:
    def test_success(self, user, mail_server):
        mail_server.EMAIL_HOST_PASSWORD = "s3cret-value"
        out = StringIO()
        call_command("send_test_email", user.email, stdout=out)
        text = out.getvalue()
        assert "mail.example.org" in text and "accepted the message" in text
        assert "s3cret-value" not in text  # the password is never printed
        assert mail.outbox[0].to == [user.email]

    def test_no_mail_server_configured(self, user, settings):
        settings.EMAIL_BACKEND = SMTP
        settings.EMAIL_CONFIGURED = False
        with pytest.raises(CommandError, match="No mail server is configured"):
            call_command("send_test_email", user.email, stdout=StringIO())

    def test_failure_names_the_cause_and_the_fix(self, user, mail_server, monkeypatch):
        from django.core.mail import EmailMessage

        def fail(self, fail_silently=False):
            raise smtplib.SMTPAuthenticationError(535, b"5.7.8 authentication failed")

        monkeypatch.setattr(EmailMessage, "send", fail)
        with pytest.raises(CommandError) as excinfo:
            call_command("send_test_email", user.email, stdout=StringIO())
        assert "MAIL_LOGIN_REJECTED" in str(excinfo.value)
        assert "What to do:" in str(excinfo.value)

    def test_warns_when_the_address_has_no_account(self, mail_server):
        out = StringIO()
        call_command("send_test_email", "stranger@example.org", stdout=out)
        assert "no account for stranger@example.org" in out.getvalue()
        assert "create_user" in out.getvalue()
