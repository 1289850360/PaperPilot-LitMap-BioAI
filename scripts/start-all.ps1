$ErrorActionPreference = "Stop"

$BackendScript = Join-Path $PSScriptRoot "start-backend.ps1"
$FrontendScript = Join-Path $PSScriptRoot "start-frontend.ps1"

Write-Host "Starting PaperPilot backend and frontend..."
Write-Host "Backend:  http://127.0.0.1:8000"
Write-Host "Frontend: http://127.0.0.1:3000"
Write-Host "Press Ctrl+C to stop both services."
Write-Host ""

$backendJob = Start-Job -Name "PaperPilotBackend" -ScriptBlock {
  param($ScriptPath)
  powershell -ExecutionPolicy Bypass -File $ScriptPath
} -ArgumentList $BackendScript

$frontendJob = Start-Job -Name "PaperPilotFrontend" -ScriptBlock {
  param($ScriptPath)
  powershell -ExecutionPolicy Bypass -File $ScriptPath
} -ArgumentList $FrontendScript

try {
  while ($true) {
    Receive-Job -Job $backendJob, $frontendJob

    $stoppedJob = @($backendJob, $frontendJob) | Where-Object { $_.State -ne "Running" }
    if ($stoppedJob.Count -gt 0) {
      Receive-Job -Job $backendJob, $frontendJob
      $names = ($stoppedJob | ForEach-Object { $_.Name }) -join ", "
      throw "One or more PaperPilot services stopped unexpectedly: $names"
    }

    Start-Sleep -Seconds 2
  }
} finally {
  Write-Host ""
  Write-Host "Stopping PaperPilot services..."
  Stop-Job -Job $backendJob, $frontendJob -ErrorAction SilentlyContinue
  Remove-Job -Job $backendJob, $frontendJob -Force -ErrorAction SilentlyContinue
}
