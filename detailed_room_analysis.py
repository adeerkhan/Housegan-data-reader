import json
import os
from collections import Counter, defaultdict
import glob

def detailed_room_analysis(directory_path):
    room_type_counts = Counter()
    room_combinations = Counter()
    files_with_room_type = defaultdict(int)
    room_types_per_file = []
    total_files = 0
    
    json_pattern = os.path.join(directory_path, "*.json")
    json_files = glob.glob(json_pattern)
    
    print(f"Performing detailed analysis on {len(json_files)} JSON files...")
    
    for i, json_file in enumerate(json_files):
        if i % 10000 == 0:
            print(f"Processed {i}/{len(json_files)} files...")
            
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                
            if 'room_type' in data:
                room_types = data['room_type']
                room_type_counts.update(room_types)
                
                # Track unique room types in this file
                unique_room_types = set(room_types)
                for room_type in unique_room_types:
                    files_with_room_type[room_type] += 1
                
                # Track room combinations (as sorted tuple)
                room_combination = tuple(sorted(unique_room_types))
                room_combinations[room_combination] += 1
                
                # Track number of room types per file
                room_types_per_file.append(len(room_types))
                
                total_files += 1
                
        except Exception as e:
            continue
            
    return room_type_counts, files_with_room_type, room_combinations, room_types_per_file, total_files

def main():
    directory_path = "rplan_json_remapped"
    
    print("Detailed Room Type Analysis")
    print("=" * 50)
    
    room_type_counts, files_with_room_type, room_combinations, room_types_per_file, total_files = detailed_room_analysis(directory_path)
    
    print(f"\nBasic Statistics:")
    print(f"Total files processed: {total_files}")
    print(f"Total rooms: {sum(room_type_counts.values())}")
    print(f"Average rooms per file: {sum(room_types_per_file) / len(room_types_per_file):.2f}")
    print(f"Min rooms in a file: {min(room_types_per_file)}")
    print(f"Max rooms in a file: {max(room_types_per_file)}")
    
    print(f"\nRoom Type Presence in Files:")
    print("-" * 40)
    sorted_presence = sorted(files_with_room_type.items(), key=lambda x: x[1], reverse=True)
    for room_type, file_count in sorted_presence:
        percentage = (file_count / total_files) * 100
        print(f"Room Type {room_type:2}: {file_count:5} files ({percentage:5.1f}%)")
    
    print(f"\nMost Common Room Type Combinations (Top 10):")
    print("-" * 50)
    most_common_combinations = room_combinations.most_common(10)
    for i, (combination, count) in enumerate(most_common_combinations, 1):
        percentage = (count / total_files) * 100
        room_types_str = ", ".join(map(str, combination))
        print(f"{i:2}. [{room_types_str}] - {count} files ({percentage:.1f}%)")
    
    # Find files with rare room types
    rare_room_types = [rt for rt, count in room_type_counts.items() if count < 1000]
    if rare_room_types:
        print(f"\nRare Room Types (< 1000 occurrences):")
        print("-" * 40)
        for room_type in sorted(rare_room_types):
            count = room_type_counts[room_type]
            file_count = files_with_room_type[room_type]
            print(f"Room Type {room_type}: {count} total, in {file_count} files")

if __name__ == "__main__":
    main()
