import os

# --- CONFIGURATION ---
IMAGE_FOLDER = r"PATH_TO_IMAGE_FOLDER"
LABEL_FOLDER = r'PATH_TO_LABEL_FOLDER'

# Supported extensions
IMG_EXTS = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
LBL_EXT = '.txt'


def sync_check_dataset():
    """
    Compares the image and label folders to ensure every image has a
    matching YOLO annotation file and vice versa.

    Returns a statistical report of matches, missing labels, and orphaned images.
    """
    if not os.path.exists(IMAGE_FOLDER) or not os.path.exists(LABEL_FOLDER):
        print("Error: One or both folders do not exist. Please check your paths.")
        return

    # 1. SCAN: Get base filenames (without extensions)
    # We use sets because they are mathematically optimized for comparison (subtraction/intersection)
    image_files = {os.path.splitext(f)[0]: f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(IMG_EXTS)}
    label_files = {os.path.splitext(f)[0]: f for f in os.listdir(LABEL_FOLDER) if f.lower().endswith(LBL_EXT)}

    image_keys = set(image_files.keys())
    label_keys = set(label_files.keys())

    # 2. ANALYZE: Find the differences
    matches = image_keys.intersection(label_keys)
    images_without_labels = image_keys - label_keys
    labels_without_images = label_keys - image_keys

    # 3. REPORTING
    print("=" * 50)
    print("       DATASET SYNC VALIDATION REPORT")
    print("=" * 50)
    print(f"Total Images found:  {len(image_keys)}")
    print(f"Total Labels found:  {len(label_keys)}")
    print(f"Perfect Matches:     {len(matches)}")
    print("-" * 30)

    if images_without_labels:
        print(f"❌ WARNING: {len(images_without_labels)} Images are missing labels!")
        print("Sample missing labels for:")
        for i, name in enumerate(list(images_without_labels)[:5]):
            print(f"  - {image_files[name]}")
        if len(images_without_labels) > 5:
            print(f"  ... and {len(images_without_labels) - 5} more.")
    else:
        print("✅ All images have matching labels.")

    print("-" * 30)

    if labels_without_images:
        print(f"❌ WARNING: {len(labels_without_images)} Labels have no matching image!")
        print("Sample orphaned labels:")
        for i, name in enumerate(list(labels_without_images)[:5]):
            print(f"  - {label_files[name]}")
        if len(labels_without_images) > 5:
            print(f"  ... and {len(labels_without_images) - 5} more.")
    else:
        print("✅ All labels have matching images.")

    print("=" * 50)

    if not images_without_labels and not labels_without_images:
        print("RESULT: Dataset is 100% synchronized and ready for training.")
    else:
        print("RESULT: Action required! Fix the orphaned files above.")


if __name__ == "__main__":
    sync_check_dataset()
