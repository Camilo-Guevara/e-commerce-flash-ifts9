<#
Creates a local virtual environment in .venv and installs requirements.

Usage (from repo root):
  powershell -ExecutionPolicy Bypass -File .\scripts\setup-python.ps1

Optional params:
  -Python "C:\\Path\\to\\python.exe"  # default: first python in PATH
  -Req ".\\requirements.txt"            # default: .\\requirements.txt
#>

param(
  [string]$Python = "python",
  [string]$Req = "requirements.txt"
)

function Ensure-Python {
  $py = (Get-Command $Python -ErrorAction SilentlyContinue)
  if (-not $py) {
    Write-Error "Python executable not found: $Python"
    exit 1
  }
}

function Ensure-Venv($pyExe) {
  if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment at .venv" -ForegroundColor Cyan
    & $pyExe -m venv .venv
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  } else {
    Write-Host ".venv already exists, skipping creation" -ForegroundColor DarkGray
  }
}

function Activate-Venv {
  $activate = ".venv\\Scripts\\Activate.ps1"
  if (-not (Test-Path $activate)) {
    Write-Error "Activation script not found at $activate"
    exit 1
  }
  Write-Host "Activating virtual environment" -ForegroundColor Cyan
  . $activate
}

function Install-Requirements($reqPath) {
  if (-not (Test-Path $reqPath)) {
    Write-Host "No requirements.txt found at $reqPath. Creating a minimal one." -ForegroundColor Yellow
    @(
      "Flask>=2.3",
      "mysql-connector-python>=8.0"
    ) | Set-Content -NoNewline:$false -Path "requirements.txt"
    $reqPath = "requirements.txt"
  }
  Write-Host "Upgrading pip" -ForegroundColor Cyan
  python -m pip install --upgrade pip
  Write-Host "Installing dependencies from $reqPath" -ForegroundColor Cyan
  pip install -r $reqPath
}

Ensure-Python
Ensure-Venv $Python
Activate-Venv
Install-Requirements $Req

Write-Host "Done. To activate later: .\\.venv\\Scripts\\Activate.ps1" -ForegroundColor Green
Write-Host "Run app: python -m src.app" -ForegroundColor Green

