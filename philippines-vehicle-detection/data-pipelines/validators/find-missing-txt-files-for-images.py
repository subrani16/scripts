import os

# --- PATH CONFIGURATION ---
# The directory containing your source images (.jpg, .png)
image_folder = r'path_to_image_folder' 
# The directory containing your generated YOLO label files (.txt)
label_folder = r'path_to_label_folder'

# 1. SCAN IMAGES: 
# Create a list of filenames without extensions (e.g., 'frame_001') 
# from the image directory, filtering for common image formats.
images = [os.path.splitext(f)[0] for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png'))]

# 2. SCAN LABELS: 
# Create a list of filenames without extensions from the label directory.
labels = [os.path.splitext(f)[0] for f in os.listdir(label_folder) if f.endswith('.txt')]

# 3. COMPARE: 
# Using Set Subtraction to find the difference.
# 'set(images) - set(labels)' returns items that are in 'images' but NOT in 'labels'.
missing = set(images) - set(labels)

# 4. REPORT:
# Output the names of images that are missing their corresponding label files.
if missing:
    print(f"❌ Found {len(missing)} images missing labels:")
    print(f"Missing labels for: {missing}")
else:
    print("✅ Success: All images have corresponding label files.")
