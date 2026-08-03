$ErrorActionPreference = "Stop"

$pythonCandidates = @(
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python312\python.exe"
)

$pythonExe = $pythonCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $pythonExe) {
    throw "Python 3.12 non trovato. Installare Python prima di avviare l'applicazione."
}

if (-not (Test-Path ".venv")) {
    & $pythonExe -m venv .venv
}

$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt

Write-Host ""
Write-Host "SIPC Genesis disponibile su http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Premere CTRL+C per arrestare il server." -ForegroundColor DarkGray
Write-Host ""

& $venvPython -m uvicorn backend.app.main:app --reload
