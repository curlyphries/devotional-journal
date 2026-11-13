# Signing in, and why a sign-in email might not arrive

Devotional Journal has no passwords. A person signs in one of four ways, and
the sign-in page only offers the ones the server actually has:

| Way in | Needs | Who it suits |
|---|---|---|
| **Emailed link** | A mail server (`EMAIL_HOST` …) | Any instance with mail |
| **Google** | `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | Public instances |
| **Link from the server log** | Nothing (`MAGIC_LINK_LOG=true`, the default when no mail server is set) | A server only you administer |
| **Link from a command** | Shell access to the server | Any instance; no mail, no log reading |

If you cloned the repository and have no mail server, the last two work out of
the box, and Google works once you add its two settings.

## Use your own mail server

Put these in the environment file (`.env.mesh`, `.env.prod` or `.env`) and
restart the backend **and** the worker:

```env
EMAIL_HOST=mail.example.org
EMAIL_PORT=587
EMAIL_HOST_USER=journal@example.org
EMAIL_HOST_PASSWORD=your-mailbox-password
DEFAULT_FROM_EMAIL=Devotional Journal <journal@example.org>
```

| Your server offers | Settings |
|---|---|
| Port 587 with STARTTLS (most common) | `EMAIL_PORT=587` |
| Port 465 with TLS from the start | `EMAIL_PORT=465` (`EMAIL_USE_SSL` turns on by itself) |
| Port 25 relay, no login | `EMAIL_PORT=25`, `EMAIL_USE_TLS=false`, leave user and password empty |

Then prove it works — this prints the settings in use (never the password),
sends one message, and if that fails says what went wrong and what to change:

```bash
docker compose --env-file .env.mesh -p dj-mesh -f docker-compose.mesh.yml exec mesh-backend python manage.py send_test_email you@example.org
```

(For the public deployment use `-f docker-compose.prod.yml exec dj-backend`;
without Docker, `python manage.py send_test_email you@example.org`.)

Once the test message arrives, set `MAGIC_LINK_LOG=false` so sign-in links stop
being written to the log.

## No mail server

**From a command** — prints a one-time link (works once, expires in 15 minutes):

```bash
docker compose --env-file .env.mesh -p dj-mesh -f docker-compose.mesh.yml exec mesh-backend python manage.py signin_link you@example.org
```

Add `--create --name "Your Name"` to create the account at the same time.

**From the log** — with no mail server configured, each requested link is
written to the worker log, and the sign-in page tells the person to ask the
administrator for it:

```bash
docker compose --env-file .env.mesh -p dj-mesh -f docker-compose.mesh.yml logs --since 5m mesh-celery
```

A sign-in link is a credential. Anyone who can read it can sign in as that
person, which is why this is off as soon as a mail server is configured.

## Who gets an account

Asking for a link does **not** create an account unless you allow it. The
answer on screen is the same either way, so nobody can use the form to find
out which addresses have accounts.

| Setting | Effect |
|---|---|
| `ALLOW_EMAIL_SIGNUP=false` (default) | Create accounts yourself: `python manage.py create_user you@example.org --name "Your Name"`. Google sign-in, if enabled, still creates accounts. |
| `ALLOW_EMAIL_SIGNUP=true` | Anyone who can reach the sign-in page can register with their own email address. Sensible on a private (mesh-only) instance. |

## "I never got the email" — checklist

Work down the list; the first match is almost always the answer.

1. **Does the sign-in page say "Ask your administrator for the link"?**
   Then no mail server is configured (`EMAIL_HOST` is empty, `localhost`, or
   the template's `smtp.example.com`). Set the mail settings above, or use a
   link from the command or the log.
2. **Is there an account for that address?** With sign-up off, a link is only
   sent to existing accounts. `send_test_email` tells you; `create_user` fixes it.
3. **Did the environment change reach the containers?** After editing the
   environment file, recreate both: `… up -d mesh-backend mesh-celery`.
4. **Run `send_test_email`.** It reports one of:

| Code | What it means | What to do |
|---|---|---|
| `MAIL_LOGIN_REJECTED` | The server refused the username or password. | Check `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD`. Many servers want the full address as the username. |
| `MAIL_RECIPIENT_REFUSED` | The server would not deliver to that address ("relay denied"). | Log in with a mailbox, or allow this server's address to relay. |
| `MAIL_SENDER_REFUSED` | The server refused the From address. | Set `DEFAULT_FROM_EMAIL` to an address that login may send as. |
| `MAIL_HELO_REJECTED` | The server rejected this machine's name. | Set `MESH_HOSTNAME` (or the container `hostname:`) to a fully qualified name. |
| `MAIL_TLS_MISMATCH` | Port and security setting do not match, or the certificate name differs. | 465 → `EMAIL_USE_SSL=true`; 587 → `EMAIL_USE_TLS=true`; `EMAIL_HOST` must be the name on the certificate. |
| `MAIL_HOST_NOT_FOUND` | The mail server name does not resolve. | Fix `EMAIL_HOST`; check DNS from inside the container. |
| `MAIL_CONNECTION_REFUSED` | Nothing is listening there. | Check host and port. Inside a container, `localhost` is the container itself — use the server's real name or `host.docker.internal`. |
| `MAIL_TIMEOUT` | No answer in `EMAIL_TIMEOUT` seconds. | A firewall is dropping the connection, or the port is wrong. |
| `MAIL_SENDER_NOT_AUTHENTICATED` | The server refused mail from your From domain sent by this machine (its answer names DMARC, SPF or DKIM). This is what an unauthenticated relay to the domain's inbound server (port 25) gets. | Log in to a mailbox on that domain's server on 587 or 465 (`EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD`). |
| `MAIL_REJECTED` | The server answered with its own error, shown verbatim. | Read it; the mail server's log has more. |

5. **The command says the server accepted the message, but nothing arrives.**
   Look in spam, then in the mail server's log. From there it is a delivery
   question (SPF/DKIM for the From domain, greylisting, a full mailbox), not a
   Devotional Journal one.

Every failed send is also written to the worker log with the same code:

```bash
docker compose --env-file .env.mesh -p dj-mesh -f docker-compose.mesh.yml logs mesh-celery | grep "NOT sent"
```

If the task queue itself is down (Redis or the worker), the backend delivers
the link directly from the request instead of leaving the person waiting.
