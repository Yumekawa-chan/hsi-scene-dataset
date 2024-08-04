import os
import json
import re
import sys
from datetime import datetime

def extract_info_from_filename(filename):
    pattern = re.compile(r"^(c?-?Scan-d\(s\d+(?:x\d+)?,g\d+,\d+\.\d+ms,\d+-\d+\)_(\d{8})_(\d{6})\.nh9)$")
    match = pattern.match(filename)
    
    if match:
        full_match = match.group(0)
        camera_params = match.group(1).split('(')[1].split(')')[0]
        date_str = match.group(2)
        time_str = match.group(3)
        has_color_checker = "c-" in full_match
        
        date_time = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
        
        return {
            "file_name": full_match,
            "date_time": date_time.strftime("%Y.%m.%d.%H.%M.%S"),
            "has_color_checker": "yes" if has_color_checker else "no",
            "camera_params": camera_params
        }
    else:
        print(f"Pattern mismatch for filename: {filename}")
    return None

def annotate_files(directory, weather):
    annotations = []
    
    for root, _, files in os.walk(directory):
        location = os.path.basename(root)
        
        for file in files:
            if file.endswith(".nh9") and "Scan-d" in file:
                file_path = os.path.join(root, file)
                file_info = extract_info_from_filename(file)
                
                if file_info:
                    file_info.update({
                        "weather": weather,
                        "location": location
                    })
                    annotations.append(file_info)
                else:
                    print(f"Skipped file due to pattern mismatch: {file_path}")
    
    return annotations

def load_existing_annotations(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    return []

def save_annotations(filepath, annotations):
    with open(filepath, 'w') as outfile:
        json.dump(annotations, outfile, indent=4)

def main():
    if len(sys.argv) != 3:
        print("Usage: python annotation.py <directory> <weather>")
        sys.exit(1)
    
    directory = sys.argv[1]
    weather = sys.argv[2]
    
    if weather not in ["sunny", "cloud", "rain", "snow"]:
        print("Weather must be one of: sunny, cloud, rain, snow")
        sys.exit(1)
    
    existing_annotations = load_existing_annotations('data.json')
    new_annotations = annotate_files(directory, weather)
    
    # Combine existing and new annotations, avoiding duplicates
    all_annotations = {ann['file_name']: ann for ann in existing_annotations}
    all_annotations.update({ann['file_name']: ann for ann in new_annotations})
    
    save_annotations('data.json', list(all_annotations.values()))

if __name__ == "__main__":
    main()
