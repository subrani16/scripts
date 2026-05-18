import json
import os


def audit_encord_json(json_path):
    """
    Scans an Encord JSON export to provide a summary of the dataset content,
    including total image counts and a frequency distribution of all object classes.
    """
    # 1. VALIDATION: Check if the file path is correct before attempting to open
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    # 2. LOADING: Read the JSON data into a Python list/dictionary structure
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Initialize counters
    class_counts = {}  # Dictionary to store { "ClassName": count }
    total_objects = 0
    total_images = 0

    # 3. TRAVERSAL: Navigate the nested Encord JSON structure
    # Root (List) -> Project (Dict) -> data_units (Dict)
    for project in data:
        data_units = project.get('data_units', {})
        
        for data_hash, content in data_units.items():
            total_images += 1
            
            # Extract the list of annotated objects for this specific image
            objects = content.get('labels', {}).get('objects', [])
            
            for obj in objects:
                # 4. TALLYING: Record the name of the object class
                name = obj.get('name', 'Unknown')
                
                # Increment the specific class count and the global object counter
                class_counts[name] = class_counts.get(name, 0) + 1
                total_objects += 1

    # 5. REPORTING: Display the findings in a clean format
    print(f"--- Audit Report for: {json_path} ---")
    print(f"Total Images:  {total_images}")
    print(f"Total Objects: {total_objects}")
    print("\nBreakdown by Class:")
    
    # Sort the results by the highest frequency first for
