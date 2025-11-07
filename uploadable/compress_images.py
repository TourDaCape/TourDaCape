#!/usr/bin/env python3
"""
Image Compression Script for Tour Da Cape Website
This script helps compress large images to make them suitable for Git repositories.
"""

import os
from PIL import Image

def compress_image(input_path, output_path, quality=80, max_width=1600, max_height=1067, format="WEBP"):
    """
    Compress an image while maintaining aspect ratio
    
    Args:
        input_path (str): Path to input image
        output_path (str): Path to save compressed image
        quality (int): JPEG quality (1-100)
        max_width (int): Maximum width in pixels
        max_height (int): Maximum height in pixels
    """
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create a white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Resize if necessary
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Save with compression (prefer WebP for best size)
            fmt = format.upper()
            if fmt == "WEBP":
                img.save(output_path, 'WEBP', quality=quality, method=6)
            elif fmt == "JPEG":
                img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            elif fmt == "PNG":
                img.save(output_path, 'PNG', optimize=True)
            else:
                img.save(output_path, 'WEBP', quality=quality, method=6)
                
        # Get file sizes
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        reduction = (1 - compressed_size / original_size) * 100
        
        print(f"Compressed: {os.path.basename(input_path)}")
        print(f"  Original: {original_size / 1024:.1f} KB")
        print(f"  Compressed: {compressed_size / 1024:.1f} KB")
        print(f"  Reduction: {reduction:.1f}%")
        print()
        
        return True
    except Exception as e:
        print(f"Error compressing {input_path}: {e}")
        return False

def compress_all_images(source_dir, target_dir, quality_webp=80, quality_jpeg=75):
    """
    Compress all images in a directory to both WebP (primary) and JPEG (fallback).
    """
    os.makedirs(target_dir, exist_ok=True)

    extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')

    for filename in os.listdir(source_dir):
        if filename.lower().endswith(extensions):
            input_path = os.path.join(source_dir, filename)
            base, _ext = os.path.splitext(filename)

            webp_out = os.path.join(target_dir, base + '.webp')
            jpeg_out = os.path.join(target_dir, base + '.jpg')

            # Compress to WebP
            compress_image(input_path, webp_out, quality=quality_webp, format="WEBP")
            # Compress to JPEG fallback
            compress_image(input_path, jpeg_out, quality=quality_jpeg, format="JPEG")

if __name__ == "__main__":
    # Define source and target directories
    source_directory = "actual-images"
    target_directory = "optimized-images"
    
    print("Tour Da Cape Image Compression Tool")
    print("=" * 40)
    print(f"Source directory: {source_directory}")
    print(f"Target directory: {target_directory}")
    print()
    
    # Check if source directory exists
    if not os.path.exists(source_directory):
        print(f"Error: Source directory '{source_directory}' not found.")
        exit(1)
    
    # Compress all images to both WebP and JPEG fallback
    compress_all_images(source_directory, target_directory, quality_webp=78, quality_jpeg=74)
    
    print("Image compression complete!")
    print(f"Optimized WebP and JPEG fallbacks saved to '{target_directory}' directory.")