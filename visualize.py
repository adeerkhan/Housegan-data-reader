import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors

# Define color mappings for different room types
ROOM_COLORS = {
    1: ('#FFB6C1', 'Living room'),      # Light pink
    2: ('#98FB98', 'Kitchen'),          # Pale green
    3: ('#87CEEB', 'Bedroom'),          # Sky blue
    4: ('#DDA0DD', 'Bathroom'),         # Plum
    5: ('#F0E68C', 'Balcony'),          # Khaki
    6: ('#FFA07A', 'Entrance'),         # Light salmon
    7: ('#E6E6FA', 'Dining room'),      # Lavender
    8: ('#FFE4B5', 'Study room'),       # Moccasin
    10: ('#D3D3D3', 'Storage'),         # Light gray
    14: ('#808080', 'Exterior wall'),   # Gray
    15: ('#8B4513', 'Front door'),      # Saddle brown
    16: ("#AD2E2E", 'Interior wall'),   # Dark gray
    17: ('#CD853F', 'Interior door')    # Peru
}

def visualize_floorplan(rms_type, fp_eds, eds_to_rms, boundary_points=None, title="Floor Plan Edges by Room Type", show_edge_labels=False):
    """
    Visualize floor plan edges (fp_eds) colored by the room types they're associated with.
    
    Args:
        rms_type: List of room types (integers 1-17)
        fp_eds: Floor plan edges as (x1, y1, x2, y2) array
        eds_to_rms: Mapping of edges to rooms
        boundary_points: Optional list of (x,y) points defining the floor plan boundary
        title: Plot title
        show_edge_labels: Whether to show edge index labels
    """
    plt.figure(figsize=(14, 12))
    plt.title(title)
    
    # Get the max dimensions to set plot limits
    x_coords = []
    y_coords = []
    
    # Add all x, y coordinates from edges
    for edge in fp_eds:
        x_coords.extend([edge[0], edge[2]])
        y_coords.extend([edge[1], edge[3]])
    
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    # Add 5% padding
    padding_x = (max_x - min_x) * 0.05
    padding_y = (max_y - min_y) * 0.05
    
    # Draw the boundary if provided
    if boundary_points and len(boundary_points) > 2:
        # Convert boundary points to x and y lists
        boundary_x = [p[0] for p in boundary_points] + [boundary_points[0][0]]
        boundary_y = [p[1] for p in boundary_points] + [boundary_points[0][1]]
        
        # Draw the boundary with a thick black line
        plt.plot(boundary_x, boundary_y, 'k-', linewidth=3.0, label='Floor Plan Boundary',
                solid_capstyle='round', zorder=1)
    
    # Create a legend mapping for each room type that appears in the data
    legend_items = {}
    
    # Draw edges with colors based on room type
    for i, edge in enumerate(fp_eds):
        x1, y1, x2, y2 = edge
        connected_rooms = eds_to_rms[i]
        
        # Default for edges not connected to any room
        color = 'black'
        linewidth = 1.5
        line_style = '-'
        alpha = 0.5
        label = None
        
        # Check if this edge connects to any room
        if connected_rooms:
            for room_idx in connected_rooms:
                if room_idx < len(rms_type):
                    room_type = rms_type[room_idx]
                    
                    # Get color and label from ROOM_COLORS
                    if room_type in ROOM_COLORS:
                        color, label_text = ROOM_COLORS[room_type]
                        linewidth = 2.5
                        alpha = 0.9
                        
                        # Only add to legend if we haven't seen this room type yet
                        if room_type not in legend_items:
                            label = f"{label_text} (Type {room_type})"
                            legend_items[room_type] = True
                        break
        
        # Draw the edge
        plt.plot([x1, x2], [y1, y2], color=color, linewidth=linewidth, 
                 linestyle=line_style, alpha=alpha, label=label, solid_capstyle='round',
                 zorder=2)  # Ensure edges are drawn on top of boundary
        
        # Add edge label if requested
        if show_edge_labels:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            plt.text(mid_x, mid_y, f"{i}", fontsize=7, ha='center', va='center',
                     bbox=dict(facecolor='white', alpha=0.7, pad=1), zorder=3)
    
    # Set plot properties
    plt.xlim(min_x - padding_x, max_x + padding_x)
    plt.ylim(min_y - padding_y, max_y + padding_y)
    plt.gca().set_aspect('equal')
    
    # Create legend without duplicates
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()

# Example usage with the data from the test.ipynb
if __name__ == "__main__":
    import json
    
    def reader(filename):
        with open(filename) as f:
            info = json.load(f)
            rms_bbs = np.array(info['boxes'], dtype=np.float32)
            fp_eds = np.array(info['edges'], dtype=np.float32)[:, :4]
            rms_type = info['room_type']
            eds_to_rms = info['ed_rm']
            return rms_type, fp_eds, rms_bbs, eds_to_rms
    
    # Example usage:
    # rms_type, fp_eds, rms_bbs, eds_to_rms = reader("data/samples/1.json")
    # visualize_floor_plan(rms_type, fp_eds, rms_bbs, eds_to_rms)
