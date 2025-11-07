# Tour Da Cape Website

A luxury tour operator website based in Cape Town, South Africa.

## Large Files Notice

This repository contains several large image files that may cause issues with Git due to size limitations. The largest files include:

- simons-town.jpg (11.8MB)
- langa-jazz.jpg (6.7MB)
- safari-adventure.jpg (4.6MB)
- table-mountain.jpg (4.1MB)

## Solutions

### Option 1: Using .gitignore (Recommended for now)
The .gitignore file excludes the large image directories from version control. Images should be hosted separately or compressed.

### Option 2: Git LFS Setup
For proper version control of large files, use Git LFS:

Windows:
```
setup_git_lfs.bat
```

Linux/Mac:
```
chmod +x setup_git_lfs.sh
./setup_git_lfs.sh
```

### Option 3: Image Optimization
Compress images using the provided Python script:

```
python compress_images.py
```

This will create a 'compressed-images' directory with smaller versions of all images.

Recommended tools for manual compression:
- TinyPNG (https://tinypng.com/)
- ImageOptim
- Squoosh

## Project Structure
- HTML pages for all website sections
- CSS styling with custom color scheme
- JavaScript for interactive elements
- Image assets in actual-images/ directory

## Deployment
Upload all files to a web server with correct file paths maintained.