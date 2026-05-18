"""
S3 Root Directory Image Sync
----------------------------
This script connects to an AWS S3 bucket and downloads files found directly 
within a specific prefix (folder), skipping any subdirectories.

The script 'flattens' the S3 directory structure by replacing slashes with 
underscores to ensure compatibility with Windows file path naming conventions.
"""

import boto3
import os

# --- CONFIGURATION ---
# The bucket name and specific prefix (folder path) to scan.
BUCKET_NAME = "S3_BUCKET_NAME"
PREFIX = "ADD_PREFIX"
LOCAL_DIR = r"PATH_TO_LOCAL_DIRECTORY"

# --- AWS CREDENTIALS ---
# WARNING: Do NOT push real keys to a public repository. 
# Use environment variables or a .env file for production.
ACCESS_KEY = "REPLACE_WITH_YOUR_ACCESS_KEY"
SECRET_KEY = "REPLACE_WITH_YOUR_SECRET_KEY"
SESSION_TOKEN = "REPLACE_WITH_YOUR_SESSION_TOKEN"


def sync_root_images_only():
    """
    Connects to S3, iterates through objects under the configured PREFIX,
    and downloads files that are located in the 'root' of that prefix.
    
    Logic:
    - Uses a Boto3 paginator to handle buckets with thousands of files.
    - Counts slashes ('/') to differentiate between root files and subfolders.
    - Flattens the local filename to prevent OS pathing errors.
    """
    # Initialize the S3 client with session-based credentials
    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN
    )

    # Ensure the local download directory exists
    if not os.path.exists(LOCAL_DIR):
        os.makedirs(LOCAL_DIR)

    # Setup the paginator to handle large buckets (S3 returns max 1000 items per call)
    paginator = s3.get_paginator('list_objects_v2')
    print(f"Connecting to S3... Filtering for files directly in {PREFIX}")

    # Determine depth of the base prefix to identify nested subfolders
    base_depth = PREFIX.count('/')

    try:
        download_count = 0
        
        # Iterate through S3 objects page by page
        for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=PREFIX):
            for obj in page.get('Contents', []):
                s3_path = obj['Key']

                # --- FILTERING LOGIC ---
                # 1. Skip the prefix itself (if it appears as an object)
                # 2. Skip if the file is inside a subfolder (check if slash count is higher)
                if s3_path == PREFIX or s3_path.count('/') > base_depth:
                    continue

                # 3. Skip if the object is empty or a directory marker
                if s3_path.endswith('/'):
                    continue

                # Flatten the filename for Windows (e.g., folder/image.jpg -> folder_image.jpg)
                local_filename = s3_path.replace('/', '_').replace('\\', '_')
                local_path = os.path.join(LOCAL_DIR, local_filename)

                # Only download if the file does not already exist locally (resume capability)
                if not os.path.exists(local_path):
                    print(f"Downloading: {s3_path}")
                    s3.download_file(BUCKET_NAME, s3_path, local_path)
                    download_count += 1

        print(f"\nSync complete! Downloaded {download_count} root-level images.")

    except Exception as e:
        print(f"An error occurred during sync: {e}")


if __name__ == "__main__":
    sync_root_images_only()
