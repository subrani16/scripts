"""Dataset Train/Validation Splitter for Object Detection.

This script randomly splits a collection of paired image (.jpg) and label 
(.txt) files from a source directory into training and validation subsets 
using an 80/20 split ratio. It creates the destination directories if they 
do not already exist.
"""

import os
import random
import shutil

# 1. Setup paths
source_dir = r"path_to_raw_images"
train_dir = r"path_to_the_train_directory"
val_dir = r"path_to_the_val_directory"

# Create the folders if they don't exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# 2. Get all image filenames (without extension)
# We assume images end in .jpg. Change to .png if needed.
images = [f[:-4] for f in os.listdir(source_dir) if f.endswith('.jpg')]

# Shuffle them so the split is random
random.shuffle(images)

# 3. Calculate the split point (80%)
split_idx = int(len(images) * 0.8)
train_list = images[:split_idx]
val_list = images[split_idx:]


def move_files(file_list, destination):
    """Copies paired image and text files to a specified destination directory.

    Iterates through a list of base filenames, locates their corresponding 
    .jpg and .txt pairs in the source directory, and copies them to the 
    target destination directory.

    Args:
        file_list (list of str): List of base filenames (without extensions) 
            to be copied.
        destination (str): The directory path where the files should be copied.

    Returns:
        None
    """
    for name in file_list:
        # Move the image
        shutil.copy(os.path.join(source_dir, name + ".jpg"), os.path.join(destination, name + ".jpg"))
        # Move the matching txt
        shutil.copy(os.path.join(source_dir, name + ".txt"), os.path.join(destination, name + ".txt"))


# 4. Execute the move
print(f"Moving {len(train_list)} images/txt pairs to {train_dir}...")
move_files(train_list, train_dir)

print(f"Moving {len(val_list)} images/txt pairs to {val_dir}...")
move_files(val_list, val_dir)

print("Done! Your data is now ready for the COCO converter.")
