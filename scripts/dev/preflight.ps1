$ErrorActionPreference = "Stop"

function Test-Command($Name) {
  return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

$checks = @(
  @{ Name = "Docker CLI"; Command = "docker"; Install = "Install Docker Desktop, then restart PowerShell." },
  @{ Name = "Node.js"; Command = "node"; Install = "Install Node.js 20+ or use the Docker Compose stack." },
  @{ Name = "npm"; Command = "npm.cmd"; Install = "Install Node.js 20+ or use the Docker Compose stack." },
  @{ Name = "Python"; Command = "python"; Install = "Install Python 3.12+ or use the Docker Compose stack." }
)

$failed = $false
foreach ($check in $checks) {
  if (Test-Command $check.Command) {
    Write-Host "[OK] $($check.Name)"
  } else {
    Write-Host "[MISSING] $($check.Name) - $($check.Install)" -ForegroundColor Yellow
    $failed = $true
  }
}

if ($failed) {
  Write-Host ""
  Write-Host "Recommended local path:" -ForegroundColor Cyan
  Write-Host "  winget install -e --id Docker.DockerDesktop"
  Write-Host "  Restart your computer or at least restart PowerShell after Docker Desktop finishes."
  exit 1
}

Write-Host ""
Write-Host "Preflight passed. You can run:" -ForegroundColor Green
Write-Host "  docker compose up --build"
