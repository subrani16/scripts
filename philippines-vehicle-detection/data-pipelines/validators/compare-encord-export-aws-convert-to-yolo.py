"""
This script performs a "Selective Copy". It looks at thousands of raw images,
finds only the ones that actually have annotations in the JSON, converts those
annotations to YOLO format, and moves both the image and the new .txt file
into a final folder together.
"""

import os
import json
import shutil

# --- CONFIGURATION ---
# Path to the source Encord JSON export
EXPORT_JSON_PATH = r"PATH_TO_EXPORT_JSON"  
# Folder containing the original pool of images (e.g., 3000+ files)
IMAGE_SOURCE_DIR = r"PATH_TO_SOURCE_DIRECTORY"  
# Destination folder where the filtered pairs (image + .txt) will be stored
OUTPUT_DIR = r"PATH_TO_OUTPUT_DIRECTORY"  

# Ontology mapping: Links Encord class names to YOLO integer IDs
class_map = {
    "jeepney": 0,
    "trike": 1
}

def convert_to_yolo():
    """
    Parses Encord JSON, filters images that contain target objects, 
    converts coordinates, and assembles a synchronized YOLO dataset.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output folder: {OUTPUT_DIR}")

    # Load the annotation data
    with open(EXPORT_JSON_PATH, 'r', encoding='utf-8') as f:
        export_data = json.load(f)

    print(f"Processing export data...")
    pair_count = 0
    missing_images = 0

    # Iterate through the projects in the export
    for row in export_data:
        data_units = row.get('data_units', {})

        for unit_hash, unit_content in data_units.items():
            # 1. FILENAME SANITIZATION
            # Replaces slashes with underscores to prevent OS path errors
            original_title = unit_content.get('data_title', '')
            safe_filename = original_title.replace('/', '_').replace('\\', '_')

            labels_container = unit_content.get('labels', {})
            yolo_lines = []

            # 2. ROBUST LABEL PARSING
            # Encord exports can vary (dicts or lists); this handles both structures
            if isinstance(labels_container, dict):
                frames = labels_container.values()
            elif isinstance(labels_container, list):
                frames = labels_container
            else:
                frames = []

            for frame_data in frames:
                # Drill down to the objects list within the frame
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
                            # 3. COORDINATE TRANSFORMATION
                            # Convert Encord (Top-Left) to YOLO (Center)
                            x, y, w, h = bbox['x'], bbox['y'], bbox['w'], bbox['h']
                            cx = x + (w / 2)
                            cy = y + (h / 2)
                            
                            # Construct the YOLO label line
                            yolo_lines.append(f"{cid} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

            # 4. DATASET ASSEMBLY
            # Only proceed if the image actually has the relevant annotations (Jeepney/Trike)
            if yolo_lines:
                source_path = os.path.join(IMAGE_SOURCE_DIR, safe_filename)

                # Check if the physical image exists in the source directory
                if os.path.exists(source_path):
                    dest_img_path = os.path.join(OUTPUT_DIR, safe_filename)
                    dest_txt_path = os.path.splitext(dest_img_path)[0] + ".txt"

                    # shutil.copy2 copies the image file AND its original metadata
                    shutil.copy2(source_path, dest_img_path)
                    
                    # Create the matching .txt annotation file
                    with open(dest_txt_path, 'w') as f_txt:
                        f_txt.write("\n".join(yolo_lines))

                    pair_count += 1
                else:
                    # Logs images defined in JSON but missing from the raw folder
                    missing_images += 1

    # --- FINAL SUMMARY ---
    print(f"\n--- Processing Complete ---")
    print(f"Successfully created: {pair_count} image/label pairs")
    print(f"Images skipped (annotated in JSON but not found in folder): {missing_images}")
    print(f"Final dataset location: {OUTPUT_DIR}")

if __name__ == "__main__":
    convert_to_yolo()
