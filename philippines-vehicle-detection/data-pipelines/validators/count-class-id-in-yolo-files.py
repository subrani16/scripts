import os

# --- CONFIGURATION ---
# Path to the folder containing your final YOLO .txt files
LABEL_FOLDER = r'PATH_TO_LABEL_FOLDER'

# Mapping of Class IDs to human-readable names for the final report
CLASS_NAMES = {
    '0': 'Jeepney',
    '1': 'Tricycle'
}


def audit_classes_and_files():
    """
    Scans YOLO label files within a directory to count occurrences of specific
    Class IDs and generates a mapping of filenames to those classes.

    The function provides:
    1. Total instances (every individual bounding box).
    2. Unique image counts (how many files contain at least one instance of a class).
    3. A sample list of filenames for manual verification.
    """
    if not os.path.exists(LABEL_FOLDER):
        print(f"Error: Folder not found at {LABEL_FOLDER}")
        return

    # Data structures to hold statistics and file lists
    # Using 'files' as a list to store the names of images where the class appears
    stats = {
        '0': {'count': 0, 'files': []},
        '1': {'count': 0, 'files': []}
    }
    total_files = 0

    # Iterate through every file in the label folder
    for filename in os.listdir(LABEL_FOLDER):
        if filename.endswith(".txt"):
            total_files += 1
            file_path = os.path.join(LABEL_FOLDER, filename)

            # Using a set to track distinct classes within a single file
            # to avoid double-counting the image itself.
            classes_in_this_file = set()

            with open(file_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if parts:
                        # YOLO format: <class_id> <x_center> <y_center> <width> <height>
                        class_id = parts[0]

                        # Increment instance count if the class is in our target map
                        if class_id in stats:
                            stats[class_id]['count'] += 1
                            classes_in_this_file.add(class_id)

            # Record this filename under each class it contains
            for cid in classes_in_this_file:
                stats[cid]['files'].append(filename)

    # --- FINAL REPORT GENERATION ---
    print("=" * 50)
    print("       YOLO CLASS & FILENAME AUDIT REPORT")
    print("=" * 50)
    print(f"Total files scanned: {total_files}\n")

    for cid, data in stats.items():
        name = CLASS_NAMES[cid]
        print(f"CLASS {cid} ({name}):")
        print(f"  - Total Instances Found: {data['count']}")
        print(f"  - Unique Images with this class: {len(data['files'])}")

        # Display the first 10 filenames as a sample for the user
        if data['files']:
            print(f"  - Filename Examples:")
            for f_name in sorted(data['files'])[:10]:
                print(f"    - {f_name}")
            if len(data['files']) > 10:
                print(f"    ... and {len(data['files']) - 10} more files.")
        print("-" * 30)


if __name__ == "__main__":
    audit_classes_and_files()
