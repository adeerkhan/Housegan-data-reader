import glob
import os
from raster_to_json import raster_to_json
from tqdm import tqdm

# Note: Adjust the SOURCE_DIR and OUTPUT_DIR path as per your directory structure.
SOURCE_DIR = r"rplan_dataset"
OUTPUT_DIR = r"rplan_json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_png_to_json(png_path):
    try:
        
        base_name = os.path.basename(png_path)
        file_name = os.path.splitext(base_name)[0]
        
    
        output_path = os.path.join(OUTPUT_DIR, f"{file_name}.json")
        raster_to_json(png_path, output_path, print_door_warning=False)
        
        return f"Successfully converted {png_path} to JSON."
    except Exception as e:
        return f"Failed to convert {png_path}. Error: {e}"

png_files = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.png")), key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))

for png_path in tqdm(png_files, desc="Converting PNG files to JSON"):
    result = convert_png_to_json(png_path)
    print(result)
