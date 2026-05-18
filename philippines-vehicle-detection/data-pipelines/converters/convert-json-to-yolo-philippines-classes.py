import json
import os

# --- 1. CONFIGURATION ---
# Path to your specific Encord JSON export file
JSON_INPUT = "Replace the path with the path to your folder" 
# Directory where the generated YOLO .txt files will be saved
OUTPUT_DIR = "Replace the path with the path to your folder" 

# --- 2. CLASS MAPPING ---
# This dictionary maps varying human-entered labels to specific YOLO integer IDs.
# Note: Both "trike" and "tricycle" are mapped to index 1 to handle inconsistent labeling.
CLASS_MAP = {
    "jeepney": 0,
    "trike": 1,  
    "tricycle": 1  
}


def convert_to_yolo():
    """
    Main function to process the JSON export and generate normalized 
    YOLO label files (.txt).
    """
    # Create output directory if it doesn't already exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Load the JSON data with UTF-8 encoding for compatibility
    with open(JSON_INPUT, 'r', encoding='utf-8') as f:
        data = json.load(f)

    file_count = 0
    object_count = 0

    # The Encord export is a list of projects; we iterate through each
    for project in data:
        # Each project has 'data_units' representing the actual files/images
        data_units = project.get('data_units', {})

        for data_hash, content in data_units.items():
            # Extract the original image name (e.g., 'car_01.jpg')
            raw_title = content.get('data_title', 'unknown')
            
            # CLEANING FILENAME:
            # Removes directory paths and strips both .jpg or .png extensions
            # to ensure the .txt filename matches the image filename exactly.
            clean_basename = os.path.basename(raw_title).split('.jpg')[0].split('.png')[0]
            label_path = os.path.join(OUTPUT_DIR, f"{clean_basename}.txt")

            yolo_lines = []
            
            # Access the nested objects list within the labels
            objects = content.get('labels', {}).get('objects', [])

            for obj in objects:
                # Normalize the label string to match our CLASS_MAP keys
                found_name = str(obj.get('name', '')).strip().lower()

                if found_name in CLASS_MAP:
                    class_id = CLASS_MAP[found_name]
                    bbox = obj.get('boundingBox', {})

                    if bbox:
                        # COORDINATE EXTRACTION:
                        # Encord provides 'x' and 'y' as the top-left corner.
                        x_tl, y_tl = bbox.get('x'), bbox.get('y')
                        w, h = bbox.get('w'), bbox.get('h')

                        # COORDINATE TRANSFORMATION:
                        # YOLO format requires the center of the box.
                        # Center = TopLeft + (Half of the Width/Height)
                        x_center = x_tl + (w / 2)
                        y_center = y_tl + (h / 2)

                        # CONSTRUCT YOLO LINE:
                        # class_id center_x center_y width height (all normalized 0-1)
                        line = f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}"
                        yolo_lines.append(line)
                        object_count += 1

            # FILE CREATION:
            # Only write the .txt file if it actually contains detected objects.
            # This prevents "empty" labels that can sometimes confuse trainers.
            if yolo_lines:
                with open(label_path, 'w') as f_out:
                    f_out.write("\n".join(yolo_lines))
                file_count += 1

    # Print summary statistics
    print(f"--- CONVERSION COMPLETE ---")
    print(f"Label files created: {file_count}")
    print(f"Total objects mapped: {object_count}")


if __name__ == "__main__":
    convert_to_yolo()
