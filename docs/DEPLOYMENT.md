# Deployment Guide

This document covers deploying the Devotional Journal stack to a production server
running Nginx, with the app served under a sub-path (e.g. `curlyphries.net/devotional-journal/`).

---

## Prerequisites

- Docker 20+ and docker-compose v1.29+ installed
- Nginx installed and managing the domain
- Host-level PostgreSQL 16 (shared with other apps on the server)
- Host-level Redis 7 (shared with other apps on the server)
- `certbot` / Let's Encrypt SSL already configured for the domain

---

## First-Time Server Setup

These steps only need to be done once per server. They are **not** automated by Docker Compose.

### 1. Create the PostgreSQL database and user

```bash
sudo -u postgres psql << 'SQL'
CREATE USER devotional_user WITH PASSWORD 'your-strong-password';
CREATE DATABASE devotional OWNER devotional_user;
SQL
```

### 2. Allow Docker containers to reach host Postgres

**`/etc/postgresql/16/main/pg_hba.conf`** — add this line:
```
host    devotional    devotional_user    172.16.0.0/12    md5
```

**`/etc/postgresql/16/main/postgresql.conf`** — ensure Postgres listens on all interfaces:
```
listen_addresses = '*'
```

Reload Postgres:
```bash
sudo systemctl restart postgresql
```

### 3. Open UFW firewall for Docker bridge network

Docker containers use the `172.16.0.0/12` subnet to reach the host.
UFW blocks this by default — open only the required ports:

```bash
# Postgres (required)
sudo ufw allow from 172.16.0.0/12 to any port 5432 comment 'PostgreSQL from Docker bridge'

# Redis (required if Redis is on the host, not in a container)
sudo ufw allow from 172.16.0.0/12 to any port 6379 comment 'Redis from Docker bridge'
```

> **Why this is needed**: UFW's default policy blocks incoming traffic on non-whitelisted ports,
> including traffic from Docker bridge networks. Without this, `host.docker.internal:5432` times
> out even though Postgres is running.

### 4. Configure Nginx

Add the following location blocks inside the `server { ... }` block for your domain,
**before** the `location /` catch-all:

```nginx
# Devotional Journal — Django API
location ^~ /devotional-journal/api/ {
    proxy_pass http://127.0.0.1:8010/api/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 120s;
}

# Devotional Journal — React SPA
location ^~ /devotional-journal {
    proxy_pass http://127.0.0.1:3010;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Test and reload:
```bash
sudo nginx -t && sudo systemctl reload nginx
```

> **Sub-path routing notes**:
> - The API location uses URI rewriting (`proxy_pass .../api/`) to strip the `/devotional-journal` prefix before Django sees it.
> - `FORCE_SCRIPT_NAME=/devotional-journal` in `.env.prod` tells Django to prepend the prefix back onto any redirects it generates.
> - `SECURE_SSL_REDIRECT=false` in `.env.prod` prevents Django from issuing HTTPS redirects on the plain-HTTP internal connection between Nginx and Gunicorn. Nginx handles SSL termination.

---

## Deploy

### 1. Clone the repository

```bash
git clone https://github.com/curlyphries/devotional-journal.git /home/curlyphries/projects/devotional-journal
cd /home/curlyphries/projects/devotional-journal
```

### 2. Create `.env.prod`

```bash
cp .env.prod.example .env.prod
chmod 600 .env.prod
```

Edit `.env.prod` and fill in all values. At minimum you must set:
- `SECRET_KEY` — generate with `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`
- `ENCRYPTION_ROOT_KEY` — generate with `python3 -c "import secrets; print(secrets.token_urlsafe(32)[:32])"`
- `POSTGRES_PASSWORD` / `DATABASE_URL` — must match what you set in step 1
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` — from Google Cloud Console
- `CORS_ALLOWED_ORIGINS` — comma-separated, no trailing comma, no empty entries

### 3. Build and start

```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

Watch the backend start (migrations run on first boot — allow ~30–60s on a fresh DB):
```bash
docker logs -f devotional-journal_dj-backend_1
```

### 4. Enable auto-start on reboot

```bash
sudo tee /etc/systemd/system/devotional-journal.service << 'EOF'
[Unit]
Description=Devotional Journal Docker Compose Stack
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/curlyphries/projects/devotional-journal
ExecStart=/usr/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.prod.yml down
User=curlyphries
Group=curlyphries

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable devotional-journal
```

---

## Updating

```bash
cd /home/curlyphries/projects/devotional-journal
git pull origin master
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

---

## Troubleshooting

### Backend fails with `connection timeout expired`

The Django container cannot reach host Postgres. Check:
1. `sudo ufw status | grep 5432` — UFW rule must exist for `172.16.0.0/12`
2. `ss -tlnp | grep 5432` — Postgres must be listening on `0.0.0.0:5432` (not just `127.0.0.1`)
3. `grep listen_addresses /etc/postgresql/*/main/postgresql.conf` — must not be `localhost`
4. `grep devotional_user /etc/postgresql/*/main/pg_hba.conf` — md5 auth entry must exist

### Backend fails with `CORS_ALLOWED_ORIGINS is missing scheme or netloc`

`.env.prod` has an empty or malformed `CORS_ALLOWED_ORIGINS`. Ensure:
- No trailing comma: `https://example.com,https://www.example.com` ✅
- Not empty: `CORS_ALLOWED_ORIGINS=` ❌ (omit entirely or provide a value)

### API returns 301 redirect to wrong path

`FORCE_SCRIPT_NAME` is not set. Django is generating redirects without the sub-path prefix.
Ensure `.env.prod` contains:
```
FORCE_SCRIPT_NAME=/devotional-journal
```

### API returns infinite redirect loop

`SECURE_SSL_REDIRECT=true` while behind a reverse proxy that speaks plain HTTP to Django.
Ensure `.env.prod` contains:
```
SECURE_SSL_REDIRECT=false
```

### Blank white page — CSS/JS blocked due to MIME type mismatch

Browser console shows:
```
The resource ".../assets/index-xxx.css" was blocked due to MIME type ("text/html") mismatch
Loading module ".../assets/index-xxx.js" was blocked because of a disallowed MIME type ("text/html")
```

The container nginx is returning `index.html` instead of the actual asset files. This happens when
`try_files $uri` resolves `/devotional-journal/assets/...` against the filesystem where the file
doesn't exist at that path (Vite outputs to `/assets/`, not `/devotional-journal/assets/`).

Ensure `frontend/nginx.conf` uses `alias` locations to strip the sub-path prefix:
```nginx
location /devotional-journal/assets/ {
    alias /usr/share/nginx/html/assets/;
}
location /devotional-journal/ {
    alias /usr/share/nginx/html/;
    try_files $uri $uri/ /index.html;
}
```

### Google Fonts blocked by Content-Security-Policy

Browser console shows:
```
Content-Security-Policy: blocked a style (style-src-elem) at https://fonts.googleapis.com/...
```

The outer Nginx CSP header doesn't include Google Fonts domains. Add them:
```nginx
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
font-src  'self' https://fonts.gstatic.com;
```

### Backend secret key warning in logs

`SECRET_KEY` was not set — Django fell back to the dev placeholder.
Regenerate and set in `.env.prod`.

---

## Port Reference

| Service | Internal port | Host binding |
|---------|--------------|--------------|
| Django (Gunicorn) | 8000 | `127.0.0.1:8010` |
| Frontend (Nginx) | 80 | `127.0.0.1:3010` |
| PostgreSQL | 5432 | host (shared) |
| Redis | 6379 | host (shared) |
| Ollama | 11434 | host (shared) |
