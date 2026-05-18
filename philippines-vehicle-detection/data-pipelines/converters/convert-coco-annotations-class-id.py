"""JSON Annotation ID Shifter.

This script modifies COCO-style JSON annotation files by decrementing 
category and annotation IDs by 1 (e.g., shifting IDs 1 and 2 to 0 and 1). 
This is commonly used when converting dataset labels from 1-based indexing 
to 0-based indexing for machine learning frameworks.
"""

import json
import os

# Define the absolute paths to your annotation files
files_to_fix = [
    # Replace the path with the path to your folder,
    # Replace the path with the path to your folder
]


def shift_ids(file_path):
    """Decrements category and annotation IDs in a JSON file by 1.

    Reads a JSON file, locates the 'categories' and 'annotations' keys,
    subtracts 1 from their respective ID fields, and overwrites the original 
    file with the updated data.

    Args:
        file_path (str): The absolute or relative path to the JSON annotation file.

    Returns:
        None
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Processing {file_path}...")

    with open(file_path, 'r') as f:
        data = json.load(f)

    # 1. Update the 'categories' section (1 -> 0, 2 -> 1)
    for category in data.get('categories', []):
        old_id = category['id']
        category['id'] -= 1
        new_id = category['id']
        print(f"  Category '{category['name']}': {old_id} -> {new_id}")

    # 2. Update the 'annotations' section (1 -> 0, 2 -> 1)
    for annotation in data.get('annotations', []):
        annotation['category_id'] -= 1

    # Save the updated JSON back to the same file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Successfully updated {file_path}\n")


if __name__ == "__main__":
    for path in files_to_fix:
        shift_ids(path)
