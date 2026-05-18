import json
import os

# --- SETTINGS ---
# Path to the exported Encord JSON annotation file
JSON_INPUT = "Replace the path with the path to your folder"  
# Destination directory for the resulting YOLO .txt label files
OUTPUT_DIR = "Replace the path with the path to your folder"

# Mapping of Encord class names to YOLO integer IDs
# YOLO requires classes to be represented as integers starting from 0
CLASS_MAP = {
    "jeepney": 0,
    "Tricycle": 1
}


def convert_to_yolo():
    """
    Parses an Encord JSON file and converts bounding box coordinates from 
    Top-Left (x, y, w, h) to YOLO Center (x_center, y_center, w, h) format.
    
    The function creates one .txt file per image containing valid objects.
    """
    # Ensure the output directory exists before starting
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Load the JSON export data
    with open(JSON_INPUT, 'r', encoding='utf-8') as f:
        data = json.load(f)

    file_count = 0
    object_count = 0

    # Iterate through each project or export entry in the JSON list
    for project in data:
        # data_units contains the individual images/frames and their labels
        data_units = project.get('data_units', {})

        for data_hash, content in data_units.items():
            # Extract the original filename and remove extensions to create the label filename
            raw_title = content.get('data_title', 'unknown')
            clean_basename = os.path.basename(raw_title).split('.jpg')[0].split('.png')[0]
            label_path = os.path.join(OUTPUT_DIR, f"{clean_basename}.txt")

            yolo_lines = []

            # Retrieve the list of labeled objects for this specific data unit
            objects = content.get('labels', {}).get('objects', [])

            for obj in objects:
                # Normalize the class name for reliable matching against CLASS_MAP
                name = str(obj.get('name', '')).lower().strip()

                if name in CLASS_MAP:
                    class_id = CLASS_MAP[name]
                    bbox = obj.get('boundingBox', {})

                    if bbox:
                        # 1. EXTRACT: Encord uses normalized (0.0 to 1.0) Top-Left coordinates
                        x_tl = bbox.get('x')  # Top-left X
                        y_tl = bbox.get('y')  # Top-left Y
                        w = bbox.get('w')     # Width
                        h = bbox.get('h')     # Height

                        # 2. TRANSFORM: Convert to YOLO format (Center X, Center Y)
                        # Formula: Center = TopLeft + (Dimension / 2)
                        x_center = x_tl + (w / 2)
                        y_center = y_tl + (h / 2)

                        # 3. FORMAT: Construct the YOLO string line
                        # Format: <class_id> <x_center> <y_center> <width> <height>
                        line = f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}"
                        yolo_lines.append(line)
                        object_count += 1

            # 4. SAVE: Only write the file if it contains at least one valid object
            if yolo_lines:
                with open(label_path, 'w') as f_out:
                    f_out.write("\n".join(yolo_lines))
                file_count += 1

    # Summary report
    print(f"--- SUCCESS ---")
    print(f"Files Created: {file_count}")
    print(f"Objects Converted: {object_count}")


if __name__ == "__main__":
    convert_to_yolo()
