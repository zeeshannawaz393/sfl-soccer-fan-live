# CI/CD Deployment — sfl.sigisolutions.net

Every push to `main` (touching `screens/**` or `build/**`) triggers
`.github/workflows/deploy.yml`, which:

1. Builds the prototype with `python build/build_proto.py`.
2. Copies `screens/sfl-prototype.html` → `dist/index.html` (the single self-contained file).
3. Uploads `dist/` to the cPanel doc root over **SSH (rsync)**.

You can also run it manually from **GitHub → Actions → Build & Deploy to cPanel (SSH) → Run workflow**.

## Required GitHub secrets

Add these under **GitHub repo → Settings → Secrets and variables → Actions → New repository secret**:

| Secret name        | Reference value / how to find it                                                                 |
|--------------------|--------------------------------------------------------------------------------------------------|
| `SSH_HOST`         | The host you SSH into — e.g. `sigisolutions.net` (or the server IP, or `sfl.sigisolutions.net`).  |
| `SSH_PORT`         | SSH port. cPanel is often `22`; many shared hosts use a custom port (check cPanel → SSH Access). If unsure, try `22`. |
| `SSH_USER`         | Your cPanel account username — from the file tree it's `sigisolutions`.                            |
| `SSH_PRIVATE_KEY`  | The **full private key** text (the one whose public half is authorized on the server). Include the `-----BEGIN OPENSSH PRIVATE KEY-----` … `-----END OPENSSH PRIVATE KEY-----` lines. |
| `SSH_TARGET_DIR`   | The subdomain document root, **with a trailing slash** — `/home/sigisolutions/sfl.sigisolutions.net/` |

## One-time server setup (authorize the key)

The **public** half of your key must be authorized on the server:

- cPanel → **SSH Access → Manage SSH Keys → Import Key** (paste the public key), then **Manage → Authorize**.
- Or append it to `~/.ssh/authorized_keys` for user `sigisolutions`.

Confirm it works locally first:

```bash
ssh -i /path/to/private_key -p <SSH_PORT> sigisolutions@<SSH_HOST> "echo ok && ls /home/sigisolutions/sfl.sigisolutions.net/"
```

## Notes
- The workflow deploys **only `index.html`** and does **not** use `--delete`, so it never overwrites an existing `.htaccess` and won't touch `cgi-bin`, `.well-known`, SSL config, or anything else already in the doc root.
- `rsync` must be available on the server (standard on cPanel SSH). If it isn't, tell me and I'll switch the deploy step to `scp`.
- After the first successful deploy, visit **https://sfl.sigisolutions.net** (enable AutoSSL in cPanel if HTTPS warns).
