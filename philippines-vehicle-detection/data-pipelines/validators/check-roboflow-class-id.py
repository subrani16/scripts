import os

# --- PATH CONFIGURATION ---
# Path to your label directory
FOLDER_PATH = 'PATH_TO_LABELS_FOLDER'


def audit_label_contents(folder_path):
    """
    Analyzes YOLO .txt files to identify empty files (background images) 
    and files that do not contain 'Class 0' (Jeepneys).
    """
    no_class_zero_files = []
    empty_files = []

    # Iterate through all files in the directory
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            # 1. CHECK FOR EMPTY FILES:
            # os.path.getsize returns 0 if the file contains no text.
            if os.path.getsize(file_path) == 0:
                empty_files.append(filename)
                continue

            has_class_zero = False
            
            # 2. CHECK FOR CLASS 0:
            with open(file_path, 'r') as f:
                for line in f:
                    # YOLO lines are space-separated: <class_id> <x> <y> <w> <h>
                    # We split the line and check if the first element is '0'
                    parts = line.strip().split()
                    if parts and parts[0] == '0':
                        has_class_zero = True
                        break

            # If the loop finished and we never found a '0', log it
            if not has_class_zero:
                no_class_zero_files.append(filename)

    # --- RESULTS REPORTING ---
    print(f"Verification Results:")
    print(f"------------------------------")
    print(f"Totally empty files (Background): {len(empty_files)}")
    print(f"Files with other classes (but missing '0'): {len(no_class_zero_files)}")
    print(f"Total non-Jeepney files: {len(empty_files) + len(no_class_zero_files)}")

    # Show examples for troubleshooting
    if no_class_zero_files:
        print("\nExamples of files with other classes:")
        for name in no_class_zero_files[:5]:  # Show first 5 examples
            print(f"- {name}")

    if empty_files:
        print("\nExamples of empty files:")
        for name in empty_files[:5]:
            print(f"- {name}")

if __name__ == "__main__":
    audit_label_contents(FOLDER_PATH)
