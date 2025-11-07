<#
Creates an 'uploadable' folder mirroring the project structure, excluding large original image folders.

Usage (PowerShell):
  .\prepare_upload_folder.ps1

Then drag-and-drop the contents of the 'uploadable' folder into GitHub's web UI.

Excluded:
  - actual-images\
  - hero-images\
  - .git\ (if present)
#>

$ErrorActionPreference = 'Stop'

# Resolve project root as the directory containing this script
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$uploadDir = Join-Path $projectRoot 'uploadable'

# Recreate uploadable directory cleanly
if (Test-Path $uploadDir) {
  Remove-Item $uploadDir -Recurse -Force
}
New-Item -ItemType Directory -Path $uploadDir | Out-Null

# Collect files excluding large/original image folders and .git
$files = Get-ChildItem -Path $projectRoot -Recurse -File |
  Where-Object {
    $_.FullName -notlike "*\actual-images\*" -and
    $_.FullName -notlike "*\hero-images\*" -and
    $_.FullName -notlike "*\.git\*" -and
    $_.FullName -ne (Join-Path $projectRoot 'upload-package.zip') -and
    $_.FullName -notlike "*\uploadable\*"
  }

if (-not $files) {
  Write-Error "No files found to include in the uploadable folder."
}

foreach ($file in $files) {
  # Compute relative path via substring to preserve tree
  $relative = $file.FullName.Substring($projectRoot.Length).TrimStart('\\')
  $dest = Join-Path $uploadDir $relative
  $destDir = Split-Path -Parent $dest
  if (-not (Test-Path $destDir)) {
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
  }
  Copy-Item -Path $file.FullName -Destination $dest -Force
}

# Report summary and size
$uploadFiles = Get-ChildItem -Path $uploadDir -Recurse -File
$sizeSum = ($uploadFiles | Measure-Object -Property Length -Sum).Sum
$sizeMB = [Math]::Round(($sizeSum / 1MB), 2)

Write-Host "Created uploadable folder: $uploadDir" -ForegroundColor Green
Write-Host "Files included: $($uploadFiles.Count)" -ForegroundColor Green
Write-Host "Total size: $sizeMB MB" -ForegroundColor Green

# Optional: list largest included images for sanity
$largestImages = $uploadFiles |
  Where-Object { $_.Extension -in @('.jpg', '.jpeg', '.png', '.webp') } |
  Sort-Object Length -Descending |
  Select-Object FullName, @{Name='KB';Expression={[Math]::Round($_.Length/1KB,1)}} -First 10

if ($largestImages) {
  Write-Host "Largest images included (Top 10):" -ForegroundColor Yellow
  foreach ($img in $largestImages) {
    Write-Host ("{0} - {1} KB" -f $img.FullName, $img.KB)
  }
}

Write-Host "Now open GitHub, create/upload your repo, and drag the CONTENTS of '$uploadDir' into the web UI." -ForegroundColor Cyan