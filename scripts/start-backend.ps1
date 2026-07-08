$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
  Write-Host "Backend virtual environment was not found. Creating it now..."
  python -m venv (Join-Path $Root ".venv")
  & $Python -m pip install --upgrade pip
  & $Python -m pip install -r (Join-Path $Root "backend\requirements.txt")
}

Set-Location (Join-Path $Root "backend")
Write-Host "Starting PaperPilot backend at http://127.0.0.1:8000"
& $Python -m uvicorn app.main:app --reload --port 8000
