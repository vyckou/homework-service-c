# homework-service-a

A minimal Flask HTTP service used as a homework/demo application. It exposes a hello endpoint and Kubernetes health probes, and is built and deployed through GitHub Actions into AWS ECR and the `homework-gitops` repository (Argo CD).

## API

| Method | Path            | Description                          |
|--------|-----------------|--------------------------------------|
| GET    | `/`             | Returns `Hello, World!`              |
| GET    | `/healthz/live` | Liveness probe (`{"status":"ok"}`)   |
| GET    | `/healthz/ready`| Readiness probe (`{"status":"ok"}`)  |

The server listens on port **8080** (`0.0.0.0`).

## Requirements

- Python 3.12+ (Docker image uses 3.12; CI lint job uses 3.14)
- [pip](https://pip.pypa.io/)

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python app.py
```

Verify:

```bash
curl http://localhost:8080/
curl http://localhost:8080/healthz/live
```

### Linting

```bash
ruff check .
ruff format --check .
```

## Docker

```bash
docker build -t homework-service-a:local .
docker run --rm -p 8080:8080 homework-service-a:local
```

## CI/CD

Workflow: [`.github/workflows/lint-test-build.yml`](.github/workflows/lint-test-build.yml)

On every pull request and push to `main`:

1. **Lint** — `ruff check` and `ruff format --check`
2. **Build** — Docker image tagged with the commit SHA

On **push to `main`**, the image is pushed to private ECR and the **staging** overlay in `homework-gitops` is updated (image tag = commit SHA).

On **git tag push**, the image is pushed and the **production** overlay is updated (image tag = tag name).

Changes to `README.md` or `changelog.md` do not trigger the workflow (`paths-ignore`).

## Deployment

Kubernetes manifests live in the separate [**homework-gitops**](https://github.com/vyckou/homework-gitops) repo under `application-manifests/homework-service-a/`. Argo CD syncs:

- **Staging** — `application-manifests/homework-service-a/staging`
- **Production** — `application-manifests/homework-service-a/prod`

The deployment runs one replica on port 8080 with liveness/readiness probes on `/healthz/live` and `/healthz/ready`. Environment-specific settings (e.g. `APP_ENV`, `LOG_LEVEL`) come from ConfigMaps in the overlay; shared config (e.g. `DB_HOST`) is in the base layer.

## Project layout

```
.
├── app.py              # Flask application
├── Dockerfile
├── pyproject.toml      # Ruff configuration
├── requirements.txt    # Runtime dependencies
├── requirements-dev.txt
└── .github/workflows/  # CI pipeline
```
