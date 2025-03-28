import argparse
import glob
import subprocess
import os
from pathlib import Path
from tqdm import tqdm

# Base directory containing PNG files
RPLAN_PATH = Path("rplan_dataset")

def paths_to_ids(paths):
    """Convert file paths to IDs by extracting the number from the filename"""
    return [int(Path(path).stem) for path in paths]

def main(limit: int | None, max_processes: int):
    # Create output directories
    output_dir = Path("rplan_json")
    failed_dir = Path("failed_rplan_json")
    output_dir.mkdir(exist_ok=True)
    failed_dir.mkdir(exist_ok=True)

    # Get all PNG files directly from rplan_dataset
    ids = paths_to_ids(glob.glob(str(RPLAN_PATH / "*.png")))

    if limit is not None:
        ids = ids[:limit]

    # Get completed and failed IDs
    done_ids = paths_to_ids(glob.glob(str(output_dir / "*.json")))  # Now expecting .json extension
    failed_ids = paths_to_ids(glob.glob(str(failed_dir / "*")))

    todo_ids = list(set(ids) - set(done_ids) - set(failed_ids))
    print(f"Number of tasks to process: {len(todo_ids)}")

    processes = set()

    for rplan_id in tqdm(todo_ids, smoothing=50/len(todo_ids) if todo_ids else 1):
        input_path = RPLAN_PATH / f"{rplan_id}.png"
        failed_marker = failed_dir / str(rplan_id)

        # Pass both the input path and the ID to raster_to_json.py
        command = (
            f'python raster_to_json.py --path "{input_path}" --id {rplan_id} || '
            f'(echo. > "{failed_marker}" && exit /b 1)'
        )

        # Start process with shell=True for Windows command execution
        process = subprocess.Popen(command, shell=True)
        processes.add(process)

        # Manage process limit
        if len(processes) >= max_processes:
            # Wait for at least one process to complete
            finished = False
            while not finished and processes:
                for p in processes.copy():
                    try:
                        if p.poll() is not None:  # Check if process has finished
                            processes.remove(p)
                            finished = True
                            break
                    except KeyboardInterrupt:
                        print("Process interrupted, cleaning up...")
                        for proc in processes:
                            proc.terminate()
                        raise

    # Wait for all remaining processes to complete
    for p in processes:
        try:
            p.wait()
        except KeyboardInterrupt:
            print("Process interrupted, cleaning up...")
            for proc in processes:
                proc.terminate()
            raise

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--limit", type=int, default=None)
    argparser.add_argument("--max_processes", type=int, default=8)

    args = argparser.parse_args()
    main(limit=args.limit, max_processes=args.max_processes)