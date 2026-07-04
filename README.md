# ASCEND OS

ASCEND OS is a production-oriented MVP scaffold for an AI Career Operating System. It uses a FastAPI modular monolith, PostgreSQL, Redis Streams, Qdrant, Celery, LangGraph, and a Next.js App Router frontend.

## Local Run

1. Copy `backend/.env.example` to `backend/.env` and set `SECRET_KEY`.
2. Run `.\scripts\dev\preflight.ps1` to confirm Docker Desktop is installed and visible to PowerShell.
3. Run `docker compose up --build`.
4. Run migrations with `docker compose exec backend alembic upgrade head`.
5. Open `http://localhost:3000/login`, create an account, generate the roadmap, and continue the first mission.

## Deployment

Use `infra/azure/deploy-container-apps.ps1` for first Azure provisioning, then `.github/workflows/deploy-azure-container-apps.yml` for image deployments.
