# Culling Helper

A simple command-line tool to help with photo culling by copying images that have corresponding .xmp files to a "Selected" folder.

## Features

- Interactive folder picker (no programming knowledge needed!)
- Automatically finds images with matching .xmp files (case-insensitive)
- Copies matched images to a "Selected" subfolder
- Supports common image formats: ARW, CR2, NEF, RAF, ORF, RW2, DNG, JPG, JPEG, TIF, TIFF, PNG, RAW

## Requirements

- Python 3.6 or higher

## Quick Setup (One Time)

Run this to create a simple alias:

```bash
cd /Users/nuno/Documents/Projects/CullingHelper
./setup_alias.sh
source ~/.zshrc
```

Now you can just type `culling` from anywhere!

## Usage

### Method 1: Using the Alias (Easiest!)

After setup, just type:
```bash
culling
```

### Method 2: Direct Command

```bash
cd /Users/nuno/Documents/Projects/CullingHelper
python3 culling_helper.py
```

### Method 3: With Folder Path

```bash
python3 culling_helper.py "/path/to/your/folder"
```

## Interactive Folder Picker

When you run the app, you'll see a simple menu:

```
📸 Culling Helper - Folder Picker
============================================================

Choose a method to select your folder:

1. Type the folder path
2. Browse from current directory
3. Use default Pictures folder
4. Exit
```

**Option 2 (Browse)** is the easiest - it lets you:
- Navigate folders by typing numbers
- Go up with `..`
- Press Enter to select the current folder
- Type `q` to cancel

## How it works

The app scans the selected folder and:
- Finds all image files (by extension)
- Finds all .xmp files
- Matches images with .xmp files by base name (case-insensitive)
- Copies matched images to a "Selected" subfolder

Example:
- Folder contains: `Image_1.ARW`, `Image_2.ARW`, `Image_2.xmp`, `Image_3.ARW`, `Image_4.ARW`, `Image_4.xmp`
- Result: Creates `Selected/` folder with `Image_2.ARW` and `Image_4.ARW`
