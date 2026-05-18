import json
import os

# --- 1. SETTINGS ---
# Path to the specific JSON file containing Tricycle annotations
JSON_INPUT = "Replace the path with the path to your folder"
# Path where the individual .txt label files will be saved
OUTPUT_DIR = "Replace the path with the path to your folder"

# --- 2. CLASS MAPPING ---
# Standardizes various label strings into a single YOLO class index (1).
# This is crucial for handling human variance in the labeling process.
CLASS_MAP = {
    "trike": 1,    # Variations found in specific JSON exports
    "tricycle": 1,
    "Tricycle": 1
}


def convert_tricycle_to_yolo():
    """
    Parses Encord data and converts normalized Top-Left bounding boxes 
    to the YOLO Center-based coordinate system.
    """
    # Ensure the destination folder exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Open and load the JSON export
    with open(JSON_INPUT, 'r', encoding='utf-8') as f:
        data = json.load(f)

    file_count = 0
    object_count = 0

    # Navigate the Encord structure: List -> project -> data_units
    for project in data:
        data_units = project.get('data_units', {})

        for data_hash, content in data_units.items():
            # Extract the image filename (e.g., tricycle_01.jpg)
            raw_title = content.get('data_title', 'unknown')

            # CLEANING: Strip paths and extensions to get just the filename
            # This ensures the .txt file matches the image name for the YOLO trainer.
            clean_basename = os.path.basename(raw_title).split('.jpg')[0].split('.png')[0]
            label_path = os.path.join(OUTPUT_DIR, f"{clean_basename}.txt")

            yolo_lines = []
            # Access the list of labeled objects for this image
            objects = content.get('labels', {}).get('objects', [])

            for obj in objects:
                # Clean up the label name (remove spaces, make lowercase)
                found_name = str(obj.get('name', '')).strip().lower()

                # Process the object only if it's a recognized tricycle variation
                if found_name in CLASS_MAP:
                    class_id = CLASS_MAP[found_name]
                    bbox = obj.get('boundingBox', {})

                    if bbox:
                        # COORDINATE MATH:
                        # Encord: x_tl, y_tl (Top-Left corner)
                        # YOLO: x_center, y_center (Geometric center)
                        x_tl, y_tl = bbox.get('x'), bbox.get('y')
                        w, h = bbox.get('w'), bbox.get('h')

                        # Calculate the center of the bounding box
                        x_center = x_tl + (w / 2)
                        y_center = y_tl + (h / 2)

                        # Create the YOLO line: <id> <x_center> <y_center> <width> <height>
                        # Values are formatted to 6 decimal places for precision
                        yolo_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")
                        object_count += 1

            # Only save a .txt file if valid tricycles were actually found in the image
            if yolo_lines:
                with open(label_path, 'w') as f_out:
                    f_out.write("\n".join(yolo_lines))
                file_count += 1

    # Print final execution stats
    print(f"--- TRICYCLE CONVERSION FINISHED ---")
    print(f"Files Created: {file_count}")
    print(f"Total Tricycles Found: {object_count}")


if __name__ == "__main__":
    convert_tricycle_to_yolo()
