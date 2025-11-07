@echo off
echo Setting up Git LFS for Tour Da Cape project...
echo.

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Git is not installed or not in PATH.
    echo Please install Git from https://git-scm.com/ and try again.
    pause
    exit /b 1
)

REM Check if Git LFS is installed
git lfs version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git LFS is not installed.
    echo Installing Git LFS...
    git lfs install
    if %errorlevel% neq 0 (
        echo Error: Failed to install Git LFS.
        echo Please install Git LFS manually from https://git-lfs.github.com/
        pause
        exit /b 1
    )
) else (
    echo Git LFS is already installed.
)

REM Set up Git LFS tracking for image files
echo Setting up Git LFS tracking for image files...
git lfs track "actual-images/*.jpg"
git lfs track "actual-images/*.jpeg"
git lfs track "actual-images/*.png"
git lfs track "actual-images/*.gif"
git lfs track "actual-images/*.webp"
git lfs track "assets/*.jpg"
git lfs track "assets/*.jpeg"
git lfs track "assets/*.png"
git lfs track "assets/*.gif"
git lfs track "assets/*.webp"

REM Add .gitattributes to Git
git add .gitattributes

echo.
echo Git LFS setup complete!
echo Large image files will now be tracked using Git LFS.
echo.
echo Next steps:
echo 1. Commit the changes: git commit -m "Setup Git LFS for large images"
echo 2. Push to remote repository: git push origin main
echo.
pause