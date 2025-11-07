<#
Creates a zip package for GitHub web upload that excludes large original image folders.

Usage (PowerShell):
  .\prepare_upload.ps1

This will create upload-package.zip in the project root, excluding:
  - actual-images\
  - hero-images\
  - .git\ (if present)

Only optimized assets, HTML/CSS/JS, and other small files are included.
#>

$ErrorActionPreference = 'Stop'

# Resolve project root as the directory containing this script
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$zipName = 'upload-package.zip'

# Collect files excluding large/original image folders and .git
$files = Get-ChildItem -Path $projectRoot -Recurse -File |
  Where-Object {
    $_.FullName -notlike "*\actual-images\*" -and
    $_.FullName -notlike "*\hero-images\*" -and
    $_.FullName -notlike "*\.git\*"
  }

if (-not $files) {
  Write-Error "No files found to include in the upload package."
}

# Build the archive
Compress-Archive -Path ($files | ForEach-Object { $_.FullName }) -DestinationPath $zipName -Force

# Report summary
$zipInfo = Get-Item -Path (Join-Path $projectRoot $zipName)
$zipSizeMB = [Math]::Round(($zipInfo.Length / 1MB), 2)

Write-Host "Created: $($zipInfo.FullName)" -ForegroundColor Green
Write-Host "Files included: $($files.Count)" -ForegroundColor Green
Write-Host "Archive size: $zipSizeMB MB" -ForegroundColor Green

# Optional: list largest included images for sanity
$largestImages = $files |
  Where-Object { $_.Extension -in @('.jpg', '.jpeg', '.png', '.webp') } |
  Sort-Object Length -Descending |
  Select-Object FullName, @{Name='KB';Expression={[Math]::Round($_.Length/1KB,1)}} -First 10

if ($largestImages) {
  Write-Host "Largest images included (Top 10):" -ForegroundColor Yellow
  foreach ($img in $largestImages) {
    Write-Host ("{0} - {1} KB" -f $img.FullName, $img.KB)
  }
}

Write-Host "Upload this zip via GitHub web interface to avoid 'file too big' errors." -ForegroundColor Cyan