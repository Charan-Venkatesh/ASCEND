$ErrorActionPreference = "Stop"
Push-Location backend
alembic upgrade head
Pop-Location
