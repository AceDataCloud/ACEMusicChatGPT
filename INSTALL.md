# Run the ACE Music task viewer

Extract the reviewed archive and install its locked runtime dependencies with Node.js 22 or newer:

```sh
tar -xzf acemusic-chatgpt.tar.gz
cd acemusic-chatgpt
npm ci --omit=dev --ignore-scripts --no-audit --no-fund
```

Use your deployment secret manager to provide the following values:

| Variable | Value |
| --- | --- |
| `PUBLIC_ORIGIN` | Public HTTPS origin of this deployment |
| `OAUTH_AUDIENCE` | The public origin followed by `/mcp` |
| `OAUTH_ISSUER`, `OAUTH_JWKS_URL` | Approved ACE OAuth issuer and HTTPS signing-key endpoint |
| `OWNED_TASK_READBACK_URL`, `OWNED_TASK_READBACK_TOKEN` | HTTPS endpoint and secret for the trusted owner- and tenant-bound task reader |
| `PORT` | Optional loopback listener port (default 8000) |

Start with `node run.mjs`. Route your HTTPS reverse proxy to the loopback listener on the same host. Check `GET /health`, then confirm `GET /.well-known/oauth-protected-resource/mcp` advertises only `acemusic.tasks:read`. The task reader must enforce the service, owner and tenant bindings described in the shared adapter. The public service API key and the protected adapter credential have distinct roles.

The archive includes its build's upstream commit in `SOURCE_COMMIT`. Its launcher selects the ACE Music profile irrespective of other process profile settings.
