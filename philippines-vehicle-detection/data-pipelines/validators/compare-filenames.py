import os


def check_filename_collisions(folder_1, folder_2):
    """
    Compares filenames between two folders and identifies duplicates 
    to prevent data loss during merging.
    """
    
    # 1. SCAN: Gather all filenames from both directories.
    # We use a 'set' because looking up items in a set is much faster than a list,
    # and it automatically ignores duplicates within the same folder.
    files_1 = set(os.listdir(folder_1))
    files_2 = set(os.listdir(folder_2))

    # 2. INTERSECT: Find filenames that exist in BOTH sets.
    # This is the "overlap" or collision point.
    collisions = files_1.intersection(files_2)

    print(f"--- Comparison Report ---")
    print(f"Folder 1 total files: {len(files_1)}")
    print(f"Folder 2 total files: {len(files_2)}")

    # 3. REPORT: If collisions exist, list them and warn the user.
    if collisions:
        print(f"\n❌ FOUND {len(collisions)} COLLISIONS:")
        
        # We sort the collisions and show a sample (first 10) to keep the console clean.
        for i, filename in enumerate(sorted(list(collisions))):
            if i < 10:
                print(f"  - {filename}")
            else:
                print(f"  ... and {len(collisions) - 10} more.")
                break # Exit loop after showing the limit

        print("\nACTION REQUIRED: You must rename these files or they will overwrite each other when merged.")
    else:
        # If the intersection was empty, it's safe to proceed.
        print("\n✅ SUCCESS: No filename collisions found.")
        print("You can safely merge these folders.")


# --- USAGE ---
# These paths point to your label directories. 
# Note the use of 'r' (raw string) to handle Windows backslashes correctly.
folder_a = r'path_to_folder_a'
folder_b = r'path_to_folder_b'

# Run the check
if __name__ == "__main__":
    check_filename_collisions(folder_a, folder_b)
