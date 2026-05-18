import os

# --- CONFIGURATION ---
# Path to your images folder
IMAGE_FOLDER = "PATH_TO_IMAGE_FOLDER"
# The prefix you want to remove
PREFIX = "ADD_PREFIX"


def rename_images_remove_prefix():
    """
    Scans the image folder and removes a specific prefix from filenames.
    Example: '_Philippines_frame_001.jpg' -> 'frame_001.jpg'
    """
    if not os.path.exists(IMAGE_FOLDER):
        print(f"Error: Folder not found at {IMAGE_FOLDER}")
        return

    files_renamed = 0
    files_skipped = 0

    print(f"Starting rename process in: {IMAGE_FOLDER}")

    for filename in os.listdir(IMAGE_FOLDER):
        # Check if the file actually starts with the prefix
        if filename.startswith(PREFIX):
            # Create the new name by removing the prefix
            new_name = filename.replace(PREFIX, "", 1)  # '1' ensures we only replace the first occurrence

            old_path = os.path.join(IMAGE_FOLDER, filename)
            new_path = os.path.join(IMAGE_FOLDER, new_name)

            # Safety Check: Don't overwrite if the target name already exists
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                files_renamed += 1
            else:
                print(f"⚠️ Skip: {new_name} already exists. Could not rename {filename}")
                files_skipped += 1
        else:
            files_skipped += 1

    print("-" * 30)
    print(f"✅ Rename Complete!")
    print(f"- Files renamed: {files_renamed}")
    print(f"- Files unchanged: {files_skipped}")
    print("-" * 30)


if __name__ == "__main__":
    rename_images_remove_prefix()
