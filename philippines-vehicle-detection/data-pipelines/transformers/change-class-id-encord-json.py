import json
import os

# --- CONFIGURATION ---
# Path to your original Encord JSON export
JSON_INPUT = "Replace the path with the path to your folder"
# Path where the updated JSON will be saved
JSON_OUTPUT = "Replace the path with the path to your folder"

# --- TARGET MAPPING ---
# Normalizing human-entered strings to your standardized YOLO-ready IDs
TARGET_MAP = {
    "jeepney": "0",
    "tricycle": "1",
    "trike": "1"
}


def refine_encord_json():
    """
    Standardizes class names and IDs within an Encord JSON file.

    This script traverses the nested dictionary structure of an Encord export,
    identifies target vehicle classes, updates their labels to a unified
    format (0 for Jeepney, 1 for Trike), and exports a new JSON while
    preserving all original metadata (hashes, titles, and coordinates).
    """
    if not os.path.exists(JSON_INPUT):
        print(f"Error: File {JSON_INPUT} not found.")
        return

    # Load the original JSON structure
    with open(JSON_INPUT, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Statistics counters for the audit report
    stats = {
        "jeepney": 0,
        "tricycle/trike": 0
    }
    ids_changed = 0

    # 1. NAVIGATE: Encord JSON root is a list of project exports
    for project in data:
        data_units = project.get('data_units', {})

        # 2. DRILL DOWN: Each data_hash represents an individual image or frame
        for data_hash, content in data_units.items():
            labels_container = content.get('labels', {})
            objects = labels_container.get('objects', [])

            # 3. IDENTIFY & MODIFY: Check each annotated object
            for obj in objects:
                # Standardize current name for consistent comparison
                original_name = str(obj.get('name', '')).strip().lower()

                if original_name in TARGET_MAP:
                    new_id = TARGET_MAP[original_name]

                    # Update report counters
                    if original_name == "jeepney":
                        stats["jeepney"] += 1
                    else:
                        stats["tricycle/trike"] += 1

                    # 4. UPDATE JSON: Apply the new naming convention
                    # We overwrite the 'name' field to ensure consistency
                    # across all labels in the updated file.
                    obj['name'] = "Jeepney" if new_id == "0" else "Tricycle"

                    ids_changed += 1

    # 5. EXPORT: Save the modified structure to a new file with clean formatting
    with open(JSON_OUTPUT, 'w', encoding='utf-8') as f_out:
        json.dump(data, f_out, indent=4)

    # --- FINAL AUDIT REPORT ---
    print("=" * 40)
    print("       JSON REFINEMENT REPORT")
    print("=" * 40)
    print(f"Total Jeepneys found:       {stats['jeepney']}")
    print(f"Total Tricycles/Trikes:    {stats['tricycle/trike']}")
    print(f"Total ID/Name changes made: {ids_changed}")
    print(f"\nNew JSON saved to: {JSON_OUTPUT}")
    print("=" * 40)


if __name__ == "__main__":
    refine_encord_json()
