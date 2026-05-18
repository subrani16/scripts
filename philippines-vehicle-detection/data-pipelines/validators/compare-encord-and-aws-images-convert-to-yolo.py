"""
Encord to YOLO Converter
------------------------
This script processes a local Encord Export JSON and matches it with 
locally downloaded images from S3 to create a YOLO-formatted dataset.

Key Features:
- Flattens filenames to handle Windows path compatibility.
- Handles multiple JSON export structures (list vs. dictionary).
- Converts Top-Left (x, y) coordinates to YOLO Center (cx, cy) format.
"""

import os
import json
import shutil

# --- CONFIGURATION ---
EXPORT_JSON_PATH = "PATH_TO_JSON_EXPORT"
IMAGE_SOURCE_DIR = "PATH_TO_SOURCE_DIRECTORY"
OUTPUT_DIR = "PATH_TO_OUTPUT_DIRECTORY"

# Map Encord ontology class names to integer IDs for YOLO
# Ensure these match your specific Encord project labels.
class_map = {
    "jeepney": 0,
    "trike": 1
}

def convert_to_yolo():
    """
    Reads the Encord export, filters for annotated images, performs 
    coordinate conversion, and organizes the image/label pairs.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output folder: {OUTPUT_DIR}")

    try:
        with open(EXPORT_JSON_PATH, 'r', encoding='utf-8') as f:
            export_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find JSON at {EXPORT_JSON_PATH}")
        return

    print(f"Processing export data...")
    pair_count = 0
    missing_images = 0

    for row in export_data:
        data_units = row.get('data_units', {})
        
        for unit_hash, unit_content in data_units.items():
            # Get filename and replace slashes with underscores for Windows file system
            original_title = unit_content.get('data_title', '')
            safe_filename = original_title.replace('/', '_').replace('\\', '_')
            
            labels_container = unit_content.get('labels', {})
            yolo_lines = []

            # --- ROBUST LABEL PARSING ---
            # Encord exports vary: some use dicts keyed by frame index, some use lists.
            if isinstance(labels_container, dict):
                frames = labels_container.values()
            elif isinstance(labels_container, list):
                frames = labels_container
            else:
                frames = []

            for frame_data in frames:
                # Handle cases where frame_data is a dict containing 'objects' or is the list itself
                if isinstance(frame_data, dict):
                    objects = frame_data.get('objects', [])
                else:
                    objects = frame_data if isinstance(frame_data, list) else []
                
                for obj in objects:
                    class_name = obj.get('name', '').lower()
                    
                    if class_name in class_map:
                        cid = class_map[class_name]
                        bbox = obj.get('boundingBox', {})
                        
                        if bbox:
                            # 1. Extract normalized top-left coordinates
                            x, y, w, h = bbox['x'], bbox['y'], bbox['w'], bbox['h']
                            
                            # 2. Convert to YOLO format (center_x, center_y, width, height)
                            cx = x + (w / 2)
                            cy = y + (h / 2)
                            yolo_lines.append(f"{cid} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

            # --- FILE MATCHING & SAVING ---
            # Only save if the image actually contains our targeted objects
            if yolo_lines:
                source_path = os.path.join(IMAGE_SOURCE_DIR, safe_filename)
                
                if os.path.exists(source_path):
                    dest_img_path = os.path.join(OUTPUT_DIR, safe_filename)
                    dest_txt_path = os.path.splitext(dest_img_path)[0] + ".txt"

                    # Copy original image to the new dataset folder
                    shutil.copy2(source_path, dest_img_path)
                    
                    # Create the matching YOLO .txt file
                    with open(dest_txt_path, 'w') as f_txt:
                        f_txt.write("\n".join(yolo_lines))
                    
                    pair_count += 1
                else:
                    # Log missing files if the S3 download didn't include them
                    missing_images += 1

    print(f"\n--- Processing Complete ---")
    print(f"Successfully created: {pair_count} image/label pairs")
    print(f"Images skipped (annotated in JSON but not found in folder): {missing_images}")
    print(f"Final dataset location: {OUTPUT_DIR}")

if __name__ == "__main__":
    convert_to_yolo()
