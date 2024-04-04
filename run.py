import glob
import os
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

from raster_to_json import raster_to_json

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

def main():
    png_files = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.png")), key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))

    # Initialize the tqdm progress bar with the total number of PNG files to convert
    with tqdm(total=len(png_files), desc="Converting PNG files to JSON") as pbar:
        with Pool(processes=cpu_count()) as pool:
            for result in pool.imap_unordered(convert_png_to_json, png_files):
                pbar.update(1)  # Update the progress bar by one for each completed conversion
                print(result)  # Print the result message

if __name__ == "__main__":
    main()
