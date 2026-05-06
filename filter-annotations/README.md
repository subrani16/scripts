# Filter Annotations by Minimum Area and Height Threshold

## Requirements

- Requires Python 3.x.
- No external libraries required (zero-dependencies).

## Usages

This script processes Encord annotation files within a specified directory and filters objects based on minimum pixel size requirements. The annotation format accepted:

- Encord native.
- `COCO.json`.

### Example Usage
```bash
python filter_annotations.py -d <input_directory/annotation_file> -o <output_directory>
```

The script will output a new directory called "" in the same -o location specified. The output directory will contain the following:

A new .json file containing filtered annotations.

The Encord JSON generated shows the following structure:

```json
{
  "labels": {
    "shape": "bounding_box",
    "name": "person",
    "objectHash": "KxD8PdOs",
    "featureHash": "od2S3a8j",
    "confidence": 1,
    "value": "person",
    "createdAt": "Fri, 20 Feb 2026 09:16:29 GMT",
    "createdBy": "username@vcatechnology.com",
    "lastEditedAt": "Fri, 20 Feb 2026 09:32:19 GMT",
    "lastEditedBy": "username@vcatechnology.com",
    "color": "#D33115",
    "manualAnnotation": true,
    "boundingBox": {
      "x": 0.7132987004106119,
      "y": 0.10424248251585516,
      "w": 0.010167049535547394,
      "h": 0.007995432674423084
    }
  }
}
```

The COCO JSON generated shows the following structure:

```json
{
  "annotations": {
    "area": 168.56286117832929,
    "bbox": [
      1369.533504788375,
      112.58188111712357,
      19.520735108250996,
      8.63506728837693
    ],
    "category_id": 1,
    "image_id": 82,
    "iscrowd": 0,
    "segmentation": [
      [
        1369.533504788375,
        112.58188111712357,
        1389.054239896626,
        112.58188111712357,
        1389.054239896626,
        121.2169484055005,
        1369.533504788375,
        121.2169484055005
      ]
    ],
    "keypoints": null,
    "num_keypoints": null,
    "id": 82,
    "attributes": {
      "track_id": 0,
      "encord_track_uuid": "KxD8PdOs",
      "classifications": {},
      "manual_annotation": true
    }
  }
}
```
