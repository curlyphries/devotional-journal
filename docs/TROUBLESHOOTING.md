# Troubleshooting

Every error the app shows has three parts:

- **what went wrong**, in a sentence,
- **what to do about it**, and
- a **code** and a **reference**, e.g. `AI_UNAVAILABLE · ref 3f9c2a1b7d4e`.

The reference is the request id. It is on every server log line for that
request, so an administrator can find exactly what happened:

```bash
docker compose -f docker-compose.prod.yml logs dj-backend | grep 3f9c2a1b7d4e
```

(Use `-p dj-mesh -f docker-compose.mesh.yml` and `mesh-backend` for the private instance.)

The same guidance is in the app under **Help → Troubleshooting**.

## Error codes

| Code | What it means | What to do |
|---|---|---|
| `VALIDATION_ERROR` | Something in the request was missing or not valid. | The message names the field. Fix it and try again. |
| `NOT_AUTHENTICATED` | Your session ended. | Sign in again. Your saved entries are untouched. |
| `PERMISSION_DENIED` | The item belongs to someone else, or needs admin rights. | Nothing to fix; go back. |
| `NOT_FOUND` | The item does not exist (often: deleted in another tab). | Go back and refresh the list. |
| `RATE_LIMITED` | Too many requests in a short time. | Wait the time shown, then retry. |
| `SERVER_ERROR` | An unexpected failure on the server. Nothing you wrote was lost unless the message says so. | Retry. If it repeats, send the reference to the administrator. |
| `NETWORK_ERROR` | The browser could not reach the server. | Check your connection. On the private instance, check you are on the mesh. |
| `TIMEOUT` | The server took too long. | Retry; local AI models can be slow on first use while they load. |
| `MESH_ONLY` | The private instance refused a client outside the mesh. | Connect to the mesh. See [MESH_DEPLOYMENT.md](MESH_DEPLOYMENT.md#problems). |
| `AI_UNAVAILABLE` | The AI provider could not be reached. Your entry is saved; you still get a scripture, chosen by built-in rules and labelled as such. | Settings → AI Provider → **Test connection**. For Ollama: is it running, and is the model pulled? Then use **Try again with AI** on the entry. |
| `AI_TIMEOUT` | The model did not answer in time. | Retry. If it keeps happening, choose a smaller model. |
| `AI_NOT_CONFIGURED` | A provider is selected but its key, model or address is missing or rejected. | Settings → AI Provider: re-enter the key or model. For Ollama the message includes the `ollama pull …` command. |
| `AI_CONSENT_REQUIRED` | The server's default AI is a cloud service and you have not allowed your text to be sent to it. | Settings → AI Provider: turn on the consent switch, or set up your own (local) provider. |
| `AI_LOCAL_ONLY` | This server only allows AI on its own network. | Choose Ollama in Settings → AI Provider. |
| `AI_BAD_RESPONSE` | The model answered with something unusable (small models do this sometimes). | Retry. If frequent, use a larger model. |
| `AI_URL_NOT_ALLOWED` | The AI server address was rejected (not http/https, unknown host, or a private address on a server that does not allow them). | Use your AI server's real address. Self-hosters: set `AI_ALLOW_PRIVATE_URLS=true`. |
| `SCRIPTURE_UNAVAILABLE` | Bible text could not be retrieved, or none of the suggested passages exist. No verse is shown rather than risk a wrong one. | Retry. Administrators: load a translation locally (below). |

## For administrators

### Is the server healthy?

```bash
curl -s http://127.0.0.1:8010/api/v1/health/
```

`{"status":"ok","checks":{"database":true,"cache":true}}` — a `false` names the
dependency that is down; the response is HTTP 503 in that case.

### Is the AI reachable for a given user?

Signed in as them, open **Settings → AI Provider**: it shows which provider
serves them, whether it runs locally or in the cloud, and the exact reason if it
cannot be used. The API behind it is `GET /api/v1/prompts/ai-status/`.

### Feedback says "AI unavailable" for everyone

1. `ollama list` on the AI host — is the model in `OLLAMA_MODEL` there? If not: `ollama pull <model>`.
2. From inside the backend container, can it reach Ollama?
   ```bash
   docker compose -f docker-compose.prod.yml exec dj-backend python -c "import httpx,os;print(httpx.get(os.environ['OLLAMA_BASE_URL']+'/api/tags').status_code)"
   ```
   Anything but `200`: fix `OLLAMA_BASE_URL`, the firewall, or set `OLLAMA_HOST=0.0.0.0:11434` for Ollama.
3. Check the log for the reason: `grep "llm call\|AI_" ` in the backend log.

### No scripture appears (`SCRIPTURE_UNAVAILABLE`)

Verse text comes from the local database first, then from `bolls.life`. If the
server has no outbound access, load a translation locally:

```bash
docker compose -f docker-compose.prod.yml exec dj-backend python manage.py load_translation WEB
```

### Nobody receives the sign-in email

The backend log says `Sign-in email could not be sent … Check EMAIL_* settings`.
Fix the `EMAIL_*` values, or on a private instance set `MAGIC_LINK_LOG=true`
and read the link from the worker log. Do not enable that on an instance where
other people can read the logs: a sign-in link is a credential.

### Entries show "unable to decrypt"

`ENCRYPTION_ROOT_KEY` differs from the one the data was written with. Restore
the original key. There is no other recovery.

### After an upgrade

```bash
docker compose -f docker-compose.prod.yml exec dj-backend python manage.py migrate
```

Settings added in this release (all optional, safe defaults): `AI_LOCAL_ONLY`,
`AI_ALLOW_PRIVATE_URLS`, `SCRIPTURE_TRANSLATIONS`, `MESH_ONLY`,
`MESH_ALLOWED_CIDRS`, `NUM_PROXIES`, `MAGIC_LINK_LOG`.
