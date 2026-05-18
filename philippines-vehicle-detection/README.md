# 🚀 The Pipeline Workflow

## 1. Pre-Processing Audit:
*  `count-objects-in-encord-annotations.py: `Before converting, run this to see a breakdown of all classes in the raw `JSON`. This helps identify typos
  (e.g., "Trike" vs "Tricycle") before they enter the training set.

## 2. Format Conversion:
*  `convert-coco-annotations-class-id.py`, `convert-json-to-yolo-philippines-classes.py`, `convert-json-to-yolo-trike-class.py`
  `convert-json-to-yolo-jeepney-class.py`: Translate Encord's normalized Top-Left $(x, y, w, h)$ coordinates into the YOLO
Center $(x_{center}, y_{center}, w, h)$ format.
*  Class 0: Jeepney.
*  Class 1: Tricycle.

## 3. Data Integrity & Validation:
*  `check-roboflow-class-id.py:` Identifies files that are either completely empty or contain objects that don't belong to Class 0 (Jeepney).
*  `compare-encord-and-aws-images-convert-to-yolo.py:` Processes a local Encord Export `JSON` and matches it with locally downloaded images from S3 to
  create a YOLO-formatted dataset.
*  `compare-encord-export-aws-convert-to-yolo.py:` It looks at thousands of raw images, finds only the ones that actually have annotations in the JSON,
  converts those annotations to YOLO format, and moves both the image and the new .txt file into a final folder together.
*  `compare-filenames.py:` Compares filenames between two folders and identifies duplicates to prevent data loss during merging.
*  `compare-images-and-yolo-files.py:` Compares the image and label folders to ensure every image has a matching `YOLO` annotation file and vice versa.
*  `count-class-id-in-yolo-files.py:` Scans `YOLO` label files within a directory to count occurrences of specific Class IDs and generates a mapping
  of filenames to those classes.
*  `find-missing-txt-files-for-images.py:` Identifies "orphaned" images that have no corresponding `.txt` label file..
*  `download-images-from-aws.py:` Connects to an AWS S3 bucket and downloads files found directly within a specific prefix (folder), skipping any
  subdirectories.
*  `split-images-yolo-annotations.py:` Randomly splits a collection of paired image (.jpg) and label (.txt) files from a source directory into
  training and validation subsets using an 80/20 split ratio.

## 4. Label Transformation
*  `change-class-id-encord-json.py`, `update-roboflow-data-class-id.py`: If merging with external datasets (like Roboflow), use this to map disparate IDs
  (e.g., changing ID 12 to ID 1) to maintain a consistent master dataset.
 *  `rename-aws-images-export.py`: renames images to match `YOLO` label annotation names.

## 🛠 Setup & Requirements

1.	Python 3.x
2.	Dependencies: No external libraries required (uses standard os, json, and math libraries).
3.	Data Security: This repository uses a .gitignore to prevent company-sensitive data from being uploaded.

## 📝 Coordinate Transformation Logic

The conversion script implements the following geometric transformation to comply with YOLO requirements:
```
$$x_{center} = x_{top\_left} + \frac{width}{2}$$
$$y_{center} = y_{top\_left} + \frac{height}{2}$$
```

## 🛡️ Privacy Note

_This is a personal portfolio project. All scripts were developed to handle proprietary data structures, but no actual company data, images, or labels are_
_included in this repository._
