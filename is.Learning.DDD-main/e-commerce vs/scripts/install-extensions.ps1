<#
Usage:
  - Open PowerShell in the repo root
  - Run:  powershell -ExecutionPolicy Bypass -File .\scripts\install-extensions.ps1
This installs all extensions listed in .vscode\extensions.txt using the VS Code `code` CLI.
#>

param(
  [string]$ListPath = ".vscode\\extensions.txt"
)

function Require-CodeCLI {
  $codeCmd = (Get-Command code -ErrorAction SilentlyContinue)
  if (-not $codeCmd) {
    Write-Host "VS Code 'code' CLI not found. Enable it from VS Code:"
    Write-Host "Command Palette -> 'Shell Command: Install 'code' command in PATH' (on Windows it is usually available by default)." -ForegroundColor Yellow
    exit 1
  }
}

if (-not (Test-Path $ListPath)) {
  Write-Error "Extensions list not found at $ListPath"
  exit 1
}

Require-CodeCLI

$exts = Get-Content $ListPath | Where-Object { $_ -and -not $_.StartsWith('#') }
if (-not $exts -or $exts.Count -eq 0) {
  Write-Host "No extensions listed in $ListPath"
  exit 0
}

foreach ($ext in $exts) {
  Write-Host "Installing extension: $ext" -ForegroundColor Cyan
  code --install-extension $ext --force | Out-Null
}

Write-Host "All extensions processed." -ForegroundColor Green

