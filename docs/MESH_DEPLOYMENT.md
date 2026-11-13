# Private instance on the mesh: `devotional-journal.curlyphries.space`

A second, separate deployment that is reachable **only from the private mesh
network** (the defaults assume a Tailscale tailnet) and whose AI runs **only on
the local network**. It shares nothing with the public deployment described in
[DEPLOYMENT.md](DEPLOYMENT.md): its own database, Redis, secrets and containers.

```
 device on the mesh ──WireGuard──► TLS proxy on the mesh: either host nginx on this
                                       │   server (listens on the mesh address only,
                                       │   allow mesh ranges / deny all) or an existing
                                       │   reverse proxy on another mesh node
                                       ▼
            127.0.0.1:3011 or <mesh ip>:3011  mesh-frontend (nginx + the web app)
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
| The TLS proxy answers on the mesh only | `deploy/mesh/nginx-devotional-journal.curlyphries.space.conf`, or your existing mesh proxy | The public interface never answers for this site. |
| `allow` mesh ranges, `deny all` | same file | Anything else on that interface gets 403. |
| Containers publish on loopback or the mesh address only | `docker-compose.mesh.yml`, `MESH_FRONTEND_BIND` | The app cannot be reached except through that proxy. |
| `MESH_ONLY=true` | forced in `docker-compose.mesh.yml` | Django refuses any client whose address is outside `MESH_ALLOWED_CIDRS`. |
| `AI_LOCAL_ONLY=true` | forced in `docker-compose.mesh.yml` | Cloud AI providers are refused for every user; journal text cannot be sent off the network by the app. |

## One-time setup

All commands run on the server, in the repository directory.

### 1. DNS

The name must resolve, for devices on the mesh, to the mesh address of whatever
terminates TLS (step 4). Either create an `A` record
`devotional-journal.curlyphries.space` → that mesh address (`tailscale ip -4`;
add an `AAAA` for the mesh IPv6 address if you use it) at your DNS provider, or
add it to the resolver your mesh already uses. A public DNS record holding a
mesh address is normal and safe: it is only reachable by devices on your mesh.
If the mesh resolver already answers every name under the domain with the
proxy's address (a wildcard or redirect zone), nothing needs to change.

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

### 4. TLS

HTTPS is required, not optional: browsers only allow the microphone (voice
entry) on a secure origin. Pick one of the two:

**A. An existing reverse proxy on the mesh already serves your domain**
(for example a Caddy that holds a `*.curlyphries.space` certificate and
proxies to other mesh nodes). Publish the frontend on this server's mesh
address instead of loopback and let that proxy terminate TLS:

```bash
# .env.mesh on this server
MESH_FRONTEND_BIND=<this server's mesh address, e.g. 100.x.y.z>
```

```caddyfile
# on the proxy node (Caddy example); it must send the real client address
@devotionaljournal host devotional-journal.curlyphries.space
handle @devotionaljournal {
	reverse_proxy <this server's mesh address>:3011 {
		header_up X-Real-IP {remote_host}
		transport http {
			read_timeout 190s
		}
	}
}
```

Step 5 (host nginx) is then not needed; skip to step 6. The frontend
container believes `X-Real-IP` only from loopback, the Docker bridge and mesh
addresses (`frontend/nginx.mesh.conf`), and the port is never on a public
address, so the proxy is the only thing that can reach it.

**B. Host nginx on this server** with its own certificate. The site is not
reachable from the internet, so Let's Encrypt must validate by DNS (`DNS-01`),
not HTTP. With certbot and your DNS provider's plugin (the example uses
Cloudflare; use the plugin for whoever hosts `curlyphries.space`):

```bash
sudo certbot certonly --dns-cloudflare --dns-cloudflare-credentials /root/.secrets/cloudflare.ini -d devotional-journal.curlyphries.space
```

### 5. Host nginx (option B only)

```bash
sudo cp deploy/mesh/nginx-devotional-journal.curlyphries.space.conf /etc/nginx/sites-available/devotional-journal.curlyphries.space
```

```bash
sudo sed -i "s/MESH_IP/$(tailscale ip -4)/g" /etc/nginx/sites-available/devotional-journal.curlyphries.space
```

```bash
sudo ln -s /etc/nginx/sites-available/devotional-journal.curlyphries.space /etc/nginx/sites-enabled/
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

### 8. Sign-in email and accounts

Sign-in links are sent through the curlyphries.space mail server. In
`.env.mesh`, fill in `EMAIL_HOST_PASSWORD` (and correct `EMAIL_HOST`,
`EMAIL_PORT` or `EMAIL_HOST_USER` if your mail server differs), then recreate
the two containers that send mail and test it:

```bash
docker compose --env-file .env.mesh -p dj-mesh -f docker-compose.mesh.yml up -d mesh-backend mesh-celery
```

```bash
docker compose --env-file .env.mesh -p dj-mesh -f docker-compose.mesh.yml exec mesh-backend python manage.py send_test_email you@curlyphries.space
```

The command prints the settings in use and, if the message cannot be sent,
what went wrong and what to change. When the test message arrives, set
`MAGIC_LINK_LOG=false` in `.env.mesh` and recreate the two containers again.

With `ALLOW_EMAIL_SIGNUP=true` (the template's default for this private
instance) anyone on the mesh can register by entering their email address on
the sign-in page. Set it to `false` to create each account yourself:

```bash
docker compose --env-file .env.mesh -p dj-mesh -f docker-compose.mesh.yml exec mesh-backend python manage.py create_user you@example.com --name "Your Name"
```

Need to get in before mail works? Create a one-time link directly:

```bash
docker compose --env-file .env.mesh -p dj-mesh -f docker-compose.mesh.yml exec mesh-backend python manage.py signin_link you@example.com --create
```

Every way of signing in, and a checklist for "I never got the email", is in
[SIGNING_IN.md](SIGNING_IN.md).

## Check that it really is private

From a device **on** the mesh:

```bash
curl -sI https://devotional-journal.curlyphries.space/ | head -1
```

Expected `HTTP/2 200`.

From a device **off** the mesh (phone on mobile data, mesh app off):

```bash
curl -m 10 -sI https://devotional-journal.curlyphries.space/ | head -1
```

Expected: no answer (timeout). Also confirm the public address does not serve it:

```bash
curl -m 10 -sI -H "Host: devotional-journal.curlyphries.space" http://<public-ip>/ | head -1
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
| Browser: site can't be reached | Device not on the mesh, or DNS not pointing at the mesh address | Connect the mesh app; `dig +short devotional-journal.curlyphries.space` should print `100.x.y.z`. |
| 403 from nginx | Client address outside the `allow` ranges | Your mesh uses another subnet: update the `allow` lines and `MESH_ALLOWED_CIDRS`. |
| 403 JSON with `"code": "MESH_ONLY"` | The proxy let it through but Django saw a non-mesh address | The TLS proxy is not sending `X-Real-IP`, or `MESH_ALLOWED_CIDRS` is wrong. |
| Sign-in mail never arrives | Usually: no mail server configured, no account for that address, or the mail server refused the message | Run `send_test_email` (step 8). It names the cause and the fix. Full checklist: [SIGNING_IN.md](SIGNING_IN.md). |
| nginx fails at boot: `cannot assign requested address` | nginx started before the mesh interface | Add the `After=tailscaled.service` override (step 5). |
| Voice button says the microphone is blocked | Page loaded over `http://` | Use `https://`; finish step 4. |
| Feedback always says "AI unavailable" | Ollama not reachable from the container | `docker compose ... exec mesh-backend python -c "import httpx;print(httpx.get('http://host.docker.internal:11434/api/tags').status_code)"` should print 200. |
