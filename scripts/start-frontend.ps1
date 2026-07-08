$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Frontend = Join-Path $Root "frontend"
$BundledDependencies = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies"
$BundledNodeDir = Join-Path $BundledDependencies "node\bin"
$BundledPnpm = Join-Path $BundledDependencies "bin\pnpm.cmd"

if (Test-Path $BundledNodeDir) {
  $env:PATH = "$BundledNodeDir;$env:PATH"
}

Set-Location $Frontend

if (-not (Test-Path "node_modules")) {
  if (Test-Path $BundledPnpm) {
    & $BundledPnpm install
  } elseif (Get-Command pnpm -ErrorAction SilentlyContinue) {
    pnpm install
  } elseif (Get-Command npm -ErrorAction SilentlyContinue) {
    npm install
  } else {
    throw "Node.js package manager not found. Install Node.js LTS and pnpm, then rerun this script."
  }
}

Write-Host "Starting PaperPilot frontend at http://127.0.0.1:3000"
node node_modules/next/dist/bin/next dev -H 127.0.0.1 -p 3000
