# Private instance on the mesh: `journal.curlyphries.space`

A second, separate deployment that is reachable **only from the private mesh
network** (the defaults assume a Tailscale tailnet) and whose AI runs **only on
the local network**. It shares nothing with the public deployment described in
[DEPLOYMENT.md](DEPLOYMENT.md): its own database, Redis, secrets and containers.

```
 device on the mesh ──WireGuard──► host nginx  (listens on the mesh address only,
                                       │        allow mesh ranges / deny all, TLS)
                                       ▼
                         127.0.0.1:3011  mesh-frontend (nginx + the web app)
                                       ▼
                                  mesh-backend (Django; MESH_ONLY re-checks the
                                       │        client address)
                    ┌──────────────────┼──────────────────┐
                 mesh-db           mesh-redis        Ollama on this host
               (Postgres)                            or another mesh node
```

## What makes it private

| Lock | Where | Effect |
|---|---|---|
| DNS points at a mesh address | your DNS provider | The name resolves to `100.x.y.z`, which is not routable on the internet. |
| nginx listens on the mesh address only | `deploy/mesh/nginx-journal.curlyphries.space.conf` | The public interface never answers for this site. |
| `allow` mesh ranges, `deny all` | same file | Anything else on that interface gets 403. |
| Containers publish on `127.0.0.1` only | `docker-compose.mesh.yml` | The app cannot be reached except through that nginx. |
| `MESH_ONLY=true` | forced in `docker-compose.mesh.yml` | Django refuses any client whose address is outside `MESH_ALLOWED_CIDRS`. |
| `AI_LOCAL_ONLY=true` | forced in `docker-compose.mesh.yml` | Cloud AI providers are refused for every user; journal text cannot be sent off the network by the app. |

## One-time setup

All commands run on the server, in the repository directory.

### 1. DNS

Create an `A` record `journal.curlyphries.space` → this server's mesh address
(`tailscale ip -4`). Add an `AAAA` record for the mesh IPv6 address if you use it.
A public DNS record holding a mesh address is normal and safe: it is only
reachable by devices on your mesh.

### 2. Environment file

```bash
cp .env.mesh.example .env.mesh
```

Fill in `SECRET_KEY`, `ENCRYPTION_ROOT_KEY` and `MESH_POSTGRES_PASSWORD` (the
file shows how to generate each). **Back up `ENCRYPTION_ROOT_KEY`** — without it
the journal entries can never be read again. If your mesh is not Tailscale, set
`MESH_ALLOWED_CIDRS` to its subnet and change the two `allow` lines in the nginx
file to match.

### 3. Start the stack

```bash
docker compose --env-file .env.mesh -p dj-mesh -f docker-compose.mesh.yml up -d --build
```

```bash
curl -s http://127.0.0.1:3011/api/v1/health/
```

Expected: `{"status": "ok", "checks": {"database": true, "cache": true}}`.

### 4. TLS certificate

The site is not reachable from the internet, so Let's Encrypt must validate by
DNS (`DNS-01`), not HTTP. With certbot and your DNS provider's plugin (the
example uses Cloudflare; use the plugin for whoever hosts `curlyphries.space`):

```bash
sudo certbot certonly --dns-cloudflare --dns-cloudflare-credentials /root/.secrets/cloudflare.ini -d journal.curlyphries.space
```

HTTPS is required, not optional: browsers only allow the microphone (voice
entry) on a secure origin.

### 5. Host nginx

```bash
sudo cp deploy/mesh/nginx-journal.curlyphries.space.conf /etc/nginx/sites-available/journal.curlyphries.space
```

```bash
sudo sed -i "s/MESH_IP/$(tailscale ip -4)/g" /etc/nginx/sites-available/journal.curlyphries.space
```

```bash
sudo ln -s /etc/nginx/sites-available/journal.curlyphries.space /etc/nginx/sites-enabled/
```

```bash
sudo nginx -t && sudo systemctl reload nginx
```

nginx must start after the mesh interface exists, or `listen 100.x.y.z` fails at
boot. With Tailscale: `sudo systemctl edit nginx` and add
`[Unit]` / `After=tailscaled.service` / `Wants=tailscaled.service`.

### 6. Local AI

Install [Ollama](https://ollama.com) on this host (or another mesh node) and
pull the model named in `.env.mesh`:

```bash
ollama pull llama3.1:8b
```

Ollama must accept connections from the containers: set
`OLLAMA_HOST=0.0.0.0:11434` in its service environment and keep port 11434
closed to the public interface in your firewall. If Ollama is on another mesh
node, set `OLLAMA_BASE_URL=http://<its mesh address>:11434`.

### 7. Scripture, offline

Load the World English Bible (public domain) into the local database so verse
lookups never leave the server:

```bash
docker compose --env-file .env.mesh -p dj-mesh -f docker-compose.mesh.yml exec mesh-backend python manage.py load_translation WEB
```

If the download fails, fetch the file on another machine and pass it with
`--file`. Without this step the app fetches each chapter from `bolls.life` on
demand (only the reference is sent, never anything a user wrote).

### 8. Create accounts and sign in

Requesting a sign-in link never creates an account by itself:

```bash
docker compose --env-file .env.mesh -p dj-mesh -f docker-compose.mesh.yml exec mesh-backend python manage.py create_user you@example.com --name "Your Name"
```

Open `https://journal.curlyphries.space` from a device on the mesh, enter that
email, then read the link from the worker log (there is no mail server):

```bash
docker compose --env-file .env.mesh -p dj-mesh -f docker-compose.mesh.yml logs --since 2m mesh-celery
```

## Check that it really is private

From a device **on** the mesh:

```bash
curl -sI https://journal.curlyphries.space/ | head -1
```

Expected `HTTP/2 200`.

From a device **off** the mesh (phone on mobile data, mesh app off):

```bash
curl -m 10 -sI https://journal.curlyphries.space/ | head -1
```

Expected: no answer (timeout). Also confirm the public address does not serve it:

```bash
curl -m 10 -sI -H "Host: journal.curlyphries.space" http://<public-ip>/ | head -1
```

Expected: your default site or an error — never the journal.

## Updating

Pushes to `master` redeploy this stack automatically when `.env.mesh` exists on
the server (see the deploy job in `.github/workflows/ci.yml`). By hand:

```bash
git pull && docker compose --env-file .env.mesh -p dj-mesh -f docker-compose.mesh.yml up -d --build
```

## Backups

```bash
docker compose --env-file .env.mesh -p dj-mesh -f docker-compose.mesh.yml exec mesh-db pg_dump -U devotional devotional | gzip > journal-$(date +%F).sql.gz
```

Keep the dump and `ENCRYPTION_ROOT_KEY` in different places; either alone is useless to a thief, both together are everything.

## Problems

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Mesh-specific:

| Symptom | Cause | Fix |
|---|---|---|
| Browser: site can't be reached | Device not on the mesh, or DNS not pointing at the mesh address | Connect the mesh app; `dig +short journal.curlyphries.space` should print `100.x.y.z`. |
| 403 from nginx | Client address outside the `allow` ranges | Your mesh uses another subnet: update the `allow` lines and `MESH_ALLOWED_CIDRS`. |
| 403 JSON with `"code": "MESH_ONLY"` | nginx let it through but Django saw a non-mesh address | The host proxy is not sending `X-Real-IP`, or `MESH_ALLOWED_CIDRS` is wrong. |
| nginx fails at boot: `cannot assign requested address` | nginx started before the mesh interface | Add the `After=tailscaled.service` override (step 5). |
| Voice button says the microphone is blocked | Page loaded over `http://` | Use `https://`; finish step 4. |
| Feedback always says "AI unavailable" | Ollama not reachable from the container | `docker compose ... exec mesh-backend python -c "import httpx;print(httpx.get('http://host.docker.internal:11434/api/tags').status_code)"` should print 200. |
