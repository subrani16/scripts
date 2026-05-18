import os

# --- CONFIGURATION ---
# Path to the folder containing your YOLO .txt label files
FOLDER_PATH = "PATH_TO_FOLDER_WITH_TXT_FILES"

# ID Mapping
ORIGINAL_ID = '0'  # The ID currently in the files (e.g., from Roboflow)
TARGET_ID = '12'   # The new ID you want to change it to (e.g., for Encord/Final Dataset)


def transform_annotations():
    """
    Iterates through all YOLO label files in a directory and updates specific 
    class IDs while preserving the original bounding box coordinates.
    """
    if not os.path.exists(FOLDER_PATH):
        print(f"Error: The folder '{FOLDER_PATH}' does not exist.")
        return

    modified_files_count = 0
    changed_lines_count = 0

    print(f"Processing files in: {FOLDER_PATH}...")

    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith(".txt"):
            file_path = os.path.join(FOLDER_PATH, filename)

            # Read the current contents of the file
            with open(file_path, 'r') as f:
                lines = f.readlines()

            new_lines = []
            file_was_changed = False

            for line in lines:
                parts = line.split()

                # VALIDATION: 
                # 1. Ensure the line follows standard YOLO format (5 columns: ID, x, y, w, h)
                # 2. Check if the first element matches the ID we want to replace
                if len(parts) == 5 and parts[0] == ORIGINAL_ID:
                    parts[0] = TARGET_ID
                    file_was_changed = True
                    changed_lines_count += 1

                # Reconstruct the line with the new ID, keeping coordinates exactly the same
                new_lines.append(" ".join(parts) + "\n")

            # Performance optimization: Only overwrite the file if a change actually occurred
            if file_was_changed:
                with open(file_path, 'w') as f:
                    f.writelines(new_lines)
                modified_files_count += 1

    # --- FINAL REPORT ---
    print("-" * 30)
    print(f"Transformation successfully completed:")
    print(f"- Files edited: {modified_files_count}")
    print(f"- Individual class labels updated: {changed_lines_count}")
    print("-" * 30)


if __name__ == "__main__":
    transform_annotations()
