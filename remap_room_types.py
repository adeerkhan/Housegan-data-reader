import json
import os
import glob
from collections import Counter

def create_room_mapping():
    """Create mapping from old room IDs to new continuous IDs"""
    # Original room types we want to keep (excluding 6 and 16) Interior wall and Entrance samples dropped
    # Sorted: [1, 2, 3, 4, 5, 7, 8, 10, 15, 17]
    original_room_types = [1, 2, 3, 4, 5, 7, 8, 10, 15, 17]
    
    # Create mapping to continuous IDs from 1 to 10 (10 room types total)
    room_mapping = {}
    for i, original_id in enumerate(sorted(original_room_types), 1):
        room_mapping[original_id] = i
    
    return room_mapping

def should_keep_file(room_types):
    """Check if file should be kept (doesn't contain room types 6 or 16)"""
    return 6 not in room_types and 16 not in room_types

def remap_room_types(room_types, mapping):
    """Remap room types using the provided mapping"""
    return [mapping[rt] for rt in room_types if rt in mapping]

def process_json_files(source_dir, target_dir):
    """Process all JSON files: filter and remap room types"""
    
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Get room mapping
    room_mapping = create_room_mapping()
    
    print("Room ID Mapping:")
    print("Old ID -> New ID | Room Name")
    print("-" * 40)
    
    # Create reverse mapping for display
    room_names = {
        1: 'Living room',
        2: 'Kitchen', 
        3: 'Bedroom',
        4: 'Bathroom',
        5: 'Balcony',
        7: 'Dining room',
        8: 'Study room',
        10: 'Storage',
        15: 'Front door',
        17: 'Interior door'
    }
    
    for old_id, new_id in room_mapping.items():
        room_name = room_names.get(old_id, 'Unknown')
        print(f"{old_id:6} -> {new_id:6} | {room_name}")
    
    # Process files
    json_pattern = os.path.join(source_dir, "*.json")
    json_files = glob.glob(json_pattern)
    
    kept_files = 0
    dropped_files = 0
    
    print(f"\nProcessing {len(json_files)} files...")
    
    for i, json_file in enumerate(json_files):
        if i % 10000 == 0:
            print(f"Processed {i}/{len(json_files)} files...")
        
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            if 'room_type' in data:
                room_types = data['room_type']
                
                # Check if we should keep this file
                if should_keep_file(room_types):
                    # Remap room types
                    new_room_types = remap_room_types(room_types, room_mapping)
                    
                    # Update the data
                    data['room_type'] = new_room_types
                    
                    # Save to target directory with same filename
                    filename = os.path.basename(json_file)
                    target_path = os.path.join(target_dir, filename)
                    
                    with open(target_path, 'w') as f:
                        json.dump(data, f)
                    
                    kept_files += 1
                else:
                    dropped_files += 1
            
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
            continue
    
    print(f"\nProcessing complete!")
    print(f"Files kept: {kept_files}")
    print(f"Files dropped: {dropped_files}")
    print(f"Drop rate: {(dropped_files / len(json_files)) * 100:.1f}%")
    
    return kept_files, dropped_files

def verify_results(target_dir, num_files_to_check=100):
    """Verify the results by checking some files"""
    json_pattern = os.path.join(target_dir, "*.json")
    json_files = glob.glob(json_pattern)
    
    if not json_files:
        print("No files found in target directory!")
        return
    
    # Check a sample of files
    import random
    sample_files = random.sample(json_files, min(num_files_to_check, len(json_files)))
    
    room_type_counts = Counter()
    
    for json_file in sample_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            if 'room_type' in data:
                room_types = data['room_type']
                room_type_counts.update(room_types)
        except:
            continue
    
    print(f"\nVerification (sample of {len(sample_files)} files):")
    print("New Room Type Distribution:")
    print("-" * 30)
    
    for room_type in sorted(room_type_counts.keys()):
        count = room_type_counts[room_type]
        percentage = (count / sum(room_type_counts.values())) * 100
        print(f"Type {room_type}: {count:4} ({percentage:5.1f}%)")

def main():
    source_dir = "Housegan-data-reader/rplan_json"
    target_dir = "Housegan-data-reader/rplan_json_remapped"
    
    print("Room Type Filtering and Remapping")
    print("=" * 50)
    print(f"Source: {source_dir}")
    print(f"Target: {target_dir}")
    print()
    print("Will drop files containing room types 6 and 16")
    print("Will remap remaining room types to continuous IDs 1-10")
    print()
    
    # Process files
    kept_files, dropped_files = process_json_files(source_dir, target_dir)
    
    # Verify results
    verify_results(target_dir)

if __name__ == "__main__":
    main()
