#!/bin/bash

echo "Setting up Git LFS for Tour Da Cape project..."
echo

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed or not in PATH."
    echo "Please install Git from https://git-scm.com/ and try again."
    exit 1
fi

# Check if Git LFS is installed
if ! command -v git-lfs &> /dev/null; then
    echo "Git LFS is not installed."
    echo "Installing Git LFS..."
    
    # Try to install Git LFS based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install git-lfs
        else
            echo "Please install Homebrew first: https://brew.sh/"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install git-lfs
        elif command -v yum &> /dev/null; then
            sudo yum install git-lfs
        elif command -v dnf &> /dev/null; then
            sudo dnf install git-lfs
        else
            echo "Please install Git LFS manually from https://git-lfs.github.com/"
            exit 1
        fi
    else
        echo "Please install Git LFS manually from https://git-lfs.github.com/"
        exit 1
    fi
    
    # Install Git LFS
    git lfs install
else
    echo "Git LFS is already installed."
    git lfs install
fi

# Set up Git LFS tracking for image files
echo "Setting up Git LFS tracking for image files..."
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

# Add .gitattributes to Git
git add .gitattributes

echo
echo "Git LFS setup complete!"
echo "Large image files will now be tracked using Git LFS."
echo
echo "Next steps:"
echo "1. Commit the changes: git commit -m \"Setup Git LFS for large images\""
echo "2. Push to remote repository: git push origin main"