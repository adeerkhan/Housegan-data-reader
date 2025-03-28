import glob
import json
import random
from pathlib import Path
import matplotlib.pyplot as plt

room_type = {
    0: "LivingRoom", 1: "MasterRoom", 2: "Kitchen", 3: "Bathroom",
    4: "DiningRoom", 5: "ChildRoom", 6: "StudyRoom", 7: "SecondRoom",
    8: "GuestRoom", 9: "Balcony", 10: "Entrance", 11: "Storage",
    12: "Wall-in", 13: "External", 14: "ExteriorWall", 15: "FrontDoor",
    16: "Unknown"
}

room_type_colors = {
    0: "orange", 1: "red", 2: "green", 3: "blue",
    4: "purple", 5: "pink", 6: "cyan", 7: "yellow",
    8: "brown", 9: "lime", 10: "magenta", 11: "gray",
    12: "olive", 13: "teal", 14: "navy", 15: "coral",
    16: "black"
}

def visualize_floorplan(json_path, ax=None, plot_title="Rplan Samples"):

    with open(json_path, 'r') as f:
        data = json.load(f)
    
    room_types = data['room_type']
    edges = data['edges']
    
    ax.set_aspect('equal')
    
    for edge in edges:
        x1, y1, x2, y2, r_type, _ = edge
        r_type = int(r_type)
        type_name = room_type.get(r_type, "Unknown")
        color = room_type_colors.get(r_type, "black")
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=2, label=type_name)
    
    all_x = [edge[0] for edge in edges] + [edge[2] for edge in edges]
    all_y = [edge[1] for edge in edges] + [edge[3] for edge in edges]
    ax.set_xlim(min(all_x) - 10, max(all_x) + 10)
    ax.set_ylim(min(all_y) - 10, max(all_y) + 10)
    
    ax.set_title(plot_title, fontsize=10)
    ax.set_xlabel("")
    ax.set_ylabel("")

def main(json_folder, num_samples=8):

    json_files = glob.glob(str(Path(json_folder) / "*.json"))
    
    if not json_files:
        print(f"No JSON files found in {json_folder}")
        return
    
    if len(json_files) < num_samples:
        print(f"Only {len(json_files)} JSON files found, using all of them.")
        selected_files = json_files
    else:
        selected_files = random.sample(json_files, num_samples)
    
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle("Random Floorplan Visualizations", fontsize=16)
    axes = axes.flatten()
    
    for idx, json_path in enumerate(selected_files):
        file_name = Path(json_path).stem
        plot_title = f"Floorplan {file_name}"
        visualize_floorplan(json_path, axes[idx], plot_title)
    
    handles, labels = axes[0].get_legend_handles_labels()
    unique_labels = list(dict.fromkeys(labels))  
    unique_handles = [handles[labels.index(lab)] for lab in unique_labels]
    fig.legend(unique_handles, unique_labels, title="Room Types", 
               loc='center right', bbox_to_anchor=(1.1, 0.5))
    
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    plt.show()

if __name__ == "__main__":
    json_folder = "rplan_json" 
    main(json_folder, num_samples=8)