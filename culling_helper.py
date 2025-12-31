#!/usr/bin/env python3
"""
Culling Helper - A simple app to copy images that have corresponding .xmp files
"""

import os
import shutil
import subprocess
from pathlib import Path
import sys


def get_image_extensions():
    """Get common image file extensions"""
    return {'.arw', '.cr2', '.nef', '.raf', '.orf', '.rw2', '.dng', '.jpg', '.jpeg', '.tif', '.tiff', '.png', '.raw'}


def pick_folder_interactive():
    """Interactive folder picker using a simple menu"""
    print("\n" + "="*60)
    print("📸 Culling Helper - Folder Picker")
    print("="*60)
    print("\nChoose a method to select your folder:\n")
    print("1. Type the folder path")
    print("2. Browse from current directory")
    print("3. Use default Pictures folder")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        path = input("\nEnter full folder path: ").strip()
        # Remove quotes if user pasted path with quotes
        path = path.strip('"').strip("'")
        return Path(path)
    
    elif choice == "2":
        return browse_folders()
    
    elif choice == "3":
        pictures = Path.home() / "Pictures"
        if pictures.exists():
            return pictures
        else:
            print(f"Pictures folder not found at {pictures}")
            return None
    
    elif choice == "4":
        print("Goodbye!")
        sys.exit(0)
    
    else:
        print("Invalid choice")
        return None


def browse_folders(start_path=None):
    """Browse folders interactively"""
    if start_path is None:
        start_path = Path.home()
    else:
        start_path = Path(start_path)
    
    while True:
        print(f"\n📁 Current directory: {start_path}")
        print("\nOptions:")
        print("  [Enter] - Select this folder")
        print("  ..      - Go up one level")
        print("  Type a number to enter that folder")
        print("  q       - Cancel")
        
        # List folders
        try:
            items = sorted(start_path.iterdir())
            folders = [item for item in items if item.is_dir() and not item.name.startswith('.')]
            
            if folders:
                print("\nFolders:")
                for i, folder in enumerate(folders[:20], 1):  # Limit to 20 folders
                    print(f"  {i}. {folder.name}/")
                
                if len(folders) > 20:
                    print(f"  ... and {len(folders) - 20} more")
            else:
                print("\n(No subfolders)")
        except PermissionError:
            print("\n(Permission denied)")
            folders = []
        
        choice = input("\nYour choice: ").strip()
        
        if choice == "":
            return start_path
        elif choice.lower() == "q":
            return None
        elif choice == "..":
            start_path = start_path.parent
        elif choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(folders):
                start_path = folders[num - 1]
            else:
                print("Invalid number")
        else:
            # Try to find folder by name
            matching = [f for f in folders if choice.lower() in f.name.lower()]
            if len(matching) == 1:
                start_path = matching[0]
            elif len(matching) > 1:
                print(f"Multiple matches found. Please be more specific.")
            else:
                # Try as direct path
                test_path = start_path / choice
                if test_path.exists() and test_path.is_dir():
                    start_path = test_path
                else:
                    print("Folder not found")


def process_images(folder_path):
    """Process images in the given folder"""
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"❌ Error: Folder does not exist: {folder_path}")
        return False
    
    if not folder_path.is_dir():
        print(f"❌ Error: Path is not a folder: {folder_path}")
        return False
    
    print(f"\n🔍 Scanning folder: {folder_path.name}")
    
    try:
        # Get all files in the folder
        all_files = list(folder_path.iterdir())
        
        # Separate image files and xmp files
        image_extensions = get_image_extensions()
        images = {}
        xmp_files = set()
        
        for file in all_files:
            if file.is_file():
                ext = file.suffix.lower()
                base_name = file.stem.lower()
                
                if ext == '.xmp':
                    xmp_files.add(base_name)
                elif ext in image_extensions:
                    images[base_name] = file
        
        # Find images that have corresponding .xmp files
        matched_images = []
        for base_name, image_file in images.items():
            if base_name in xmp_files:
                matched_images.append(image_file)
        
        if not matched_images:
            print("❌ No images with corresponding .xmp files found")
            return False
        
        print(f"✅ Found {len(matched_images)} image(s) with .xmp files")
        
        # Create Selected folder
        selected_folder = folder_path / "Selected"
        selected_folder.mkdir(exist_ok=True)
        
        # Copy matched images
        print(f"\n📋 Copying images to: {selected_folder}")
        copied_count = 0
        for image_file in matched_images:
            dest_path = selected_folder / image_file.name
            shutil.copy2(image_file, dest_path)
            print(f"  ✓ {image_file.name}")
            copied_count += 1
        
        print(f"\n🎉 Success! Copied {copied_count} image(s) to '{selected_folder}'")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Main function"""
    # Check if folder path provided as argument
    if len(sys.argv) > 1:
        folder_path = Path(sys.argv[1])
    else:
        folder_path = pick_folder_interactive()
    
    if folder_path is None:
        print("No folder selected. Exiting.")
        sys.exit(1)
    
    success = process_images(folder_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
