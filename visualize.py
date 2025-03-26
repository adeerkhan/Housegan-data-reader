import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, PathPatch
from matplotlib.collections import PatchCollection
import matplotlib.colors as mcolors
import matplotlib.path as mpath
from PIL import Image

# Define color mappings for different room types based on the ROOM_TYPE_CONVERSION mapping
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
    16: ('#A9A9A9', 'Interior wall'),   # Dark gray
    17: ('#CD853F', 'Interior door')    # Peru
}

def visualize_room_types(img, title="Floor Plan Room Types"):
    """
    Visualize room types from the input image.
    Args:
        img: Input image array with shape (256, 256, 3)
        title: Plot title
    """
    # Extract room types from channel 2
    room_types = img[:, :, 1]
    
    # Create a colormap for room types
    unique_types = np.unique(room_types)
    colors = [ROOM_COLORS.get(i, ('#FFFFFF', 'Unknown'))[0] for i in range(max(unique_types) + 1)]
    cmap = mcolors.ListedColormap(colors)
    
    plt.figure(figsize=(12, 8))
    plt.imshow(room_types, cmap=cmap)
    
    # Create legend
    legend_elements = [plt.Rectangle((0, 0), 1, 1, facecolor=ROOM_COLORS.get(i, ('#FFFFFF', 'Unknown'))[0], 
                                   label=ROOM_COLORS.get(i, ('#FFFFFF', 'Unknown'))[1]) 
                      for i in unique_types if i in ROOM_COLORS]
    plt.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def visualize_walls_and_doors(walls, doors, size=256, title="Walls and Doors"):
    """
    Visualize walls and doors from the processed data.
    Args:
        walls: List of wall coordinates and types
        doors: List of door coordinates
        size: Image size (default 256)
        title: Plot title
    """
    plt.figure(figsize=(12, 8))
    
    # Plot walls
    for wall in walls:
        x = [wall[0], wall[2]]
        y = [wall[1], wall[3]]
        wall_type = wall[5]
        color = ROOM_COLORS.get(wall_type, ('#000000', 'Unknown'))[0]
        plt.plot(x, y, color=color, linewidth=2)
    
    # Plot doors
    for door in doors:
        x = [door[0], door[2]]
        y = [door[1], door[3]]
        plt.plot(x, y, color='#8B4513', linewidth=3, linestyle='--')
    
    plt.title(title)
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.show()

def visualize_full_floorplan(img, walls, doors, title="Complete Floor Plan"):
    """
    Visualize the complete floor plan with rooms, walls, and doors.
    Args:
        img: Input image array
        walls: List of wall coordinates and types
        doors: List of door coordinates
        title: Plot title
    """
    plt.figure(figsize=(15, 10))
    
    # Plot room types
    room_types = img[:, :, 1]
    unique_types = np.unique(room_types)
    colors = [ROOM_COLORS.get(i, ('#FFFFFF', 'Unknown'))[0] for i in range(max(unique_types) + 1)]
    cmap = mcolors.ListedColormap(colors)
    plt.imshow(room_types, cmap=cmap, alpha=0.5)
    
    # Plot walls
    for wall in walls:
        x = [wall[0], wall[2]]
        y = [wall[1], wall[3]]
        wall_type = wall[5]
        color = ROOM_COLORS.get(wall_type, ('#000000', 'Unknown'))[0]
        plt.plot(x, y, color=color, linewidth=2)
    
    # Plot doors
    for door in doors:
        x = [door[0], door[2]]
        y = [door[1], door[3]]
        plt.plot(x, y, color='#8B4513', linewidth=3, linestyle='--')
    
    # Create legend
    legend_elements = [plt.Rectangle((0, 0), 1, 1, facecolor=ROOM_COLORS.get(i, ('#FFFFFF', 'Unknown'))[0], 
                                   label=ROOM_COLORS.get(i, ('#FFFFFF', 'Unknown'))[1]) 
                      for i in unique_types if i in ROOM_COLORS]
    plt.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def visualize_channels(img, title="Image Channels"):
    """
    Visualize all channels of the input image separately.
    Args:
        img: Input image array with shape (256, 256, 3)
        title: Plot title
    """
    channel_names = ['Wall Types (Channel 1)', 'Room Types (Channel 2)', 'Room Numbers (Channel 3)']
    
    plt.figure(figsize=(15, 5))
    plt.suptitle(title)
    
    for i in range(3):
        plt.subplot(1, 3, i+1)
        plt.imshow(img[:, :, i], cmap='tab20')
        plt.title(channel_names[i])
        plt.axis('off')
        plt.colorbar()
    
    plt.tight_layout()
    plt.show()

def visualize_extracted_floorplan(rm_type, poly, doors, walls, title="Extracted Floor Plan", size=256):
    """
    Visualize the extracted floor plan data.
    Args:
        rm_type: List of room types
        poly: List of polygon vertex counts
        doors: List of door coordinates
        walls: List of wall coordinates and types
        title: Plot title
        size: Image size (default 256)
    """
    plt.figure(figsize=(15, 10))
    
    # Create a dictionary to store walls by room type
    walls_by_type = {}
    for wall in walls:
        wall_type = wall[5]  # Get wall type
        if wall_type not in walls_by_type:
            walls_by_type[wall_type] = []
        walls_by_type[wall_type].append(wall)
    
    # Plot walls by type
    for wall_type in walls_by_type:
        type_walls = walls_by_type[wall_type]
        color = ROOM_COLORS.get(wall_type, ('#000000', 'Unknown'))[0]
        label = ROOM_COLORS.get(wall_type, ('#000000', 'Unknown'))[1]
        
        # Plot walls of this type
        for wall in type_walls:
            x = [wall[0], wall[2]]
            y = [wall[1], wall[3]]
            plt.plot(x, y, color=color, linewidth=2, label=label)
            
            # Remove duplicate labels
            handles, labels = plt.gca().get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            plt.legend(by_label.values(), by_label.keys(), 
                      bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Plot doors with different styles for interior and front doors
    for i, door in enumerate(doors):
        x = [door[0], door[2]]
        y = [door[1], door[3]]
        # Check if this is a front door (every 4th door coordinate set)
        if (i // 4) == len(doors) // 4 - 1:  # Last door is front door
            plt.plot(x, y, color='#8B4513', linewidth=3, linestyle='--', label='Front Door')
        else:
            plt.plot(x, y, color='#CD853F', linewidth=2, linestyle=':', label='Interior Door')
    
    # Add room type labels
    for i, wall_group in enumerate(walls_by_type.values()):
        if len(wall_group) > 0:
            # Calculate center point of the room
            x_coords = [w[0] for w in wall_group] + [w[2] for w in wall_group]
            y_coords = [w[1] for w in wall_group] + [w[3] for w in wall_group]
            center_x = sum(x_coords) / len(x_coords)
            center_y = sum(y_coords) / len(y_coords)
            
            # Add room type label if it's a room (not a wall or door)
            room_type = wall_group[0][5]
            if room_type in ROOM_COLORS and room_type not in [14, 15, 16, 17]:
                plt.text(center_x, center_y, ROOM_COLORS[room_type][1],
                        horizontalalignment='center',
                        verticalalignment='center',
                        fontsize=8,
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    plt.title(title)
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Remove duplicate legend entries
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), 
              bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()

def visualize_room_connectivity(walls, doors, size=256, title="Room Connectivity"):
    """
    Visualize the connectivity between rooms through doors.
    Args:
        walls: List of wall coordinates and types
        doors: List of door coordinates
        size: Image size (default 256)
        title: Plot title
    """
    plt.figure(figsize=(12, 8))
    
    # Plot walls in light gray
    for wall in walls:
        x = [wall[0], wall[2]]
        y = [wall[1], wall[3]]
        plt.plot(x, y, color='#CCCCCC', linewidth=1)
    
    # Plot doors with different colors and thicker lines
    colors = plt.cm.rainbow(np.linspace(0, 1, len(doors)//4))
    for i in range(0, len(doors), 4):
        door_coords = doors[i:i+4]
        color = colors[i//4]
        
        # Plot each door segment
        for j in range(len(door_coords)):
            x = [door_coords[j][0], door_coords[j][2]]
            y = [door_coords[j][1], door_coords[j][3]]
            plt.plot(x, y, color=color, linewidth=3)
    
    plt.title(title)
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.show()

def visualize_filled_floorplan(rm_type, walls, doors, title="Filled Floor Plan", size=256):
    """
    Visualize the extracted floor plan with filled rooms.
    Args:
        rm_type: List of room types
        walls: List of wall coordinates and types
        doors: List of door coordinates
        title: Plot title
        size: Image size (default 256)
    """
    plt.figure(figsize=(15, 10))
    
    # Group walls by room id (wall[6] is the room id)
    rooms_by_id = {}
    for wall in walls:
        room_id = wall[6]
        
        # Skip walls
        if wall[5] in [14, 15, 16, 17]:
            continue
            
        if room_id not in rooms_by_id:
            rooms_by_id[room_id] = []
        
        # Add vertices
        rooms_by_id[room_id].append((wall[0], wall[1]))
        rooms_by_id[room_id].append((wall[2], wall[3]))
    
    # Plot each room as a filled polygon
    for room_id, vertices in rooms_by_id.items():
        # Find unique vertices to create polygon
        unique_vertices = []
        for vertex in vertices:
            if vertex not in unique_vertices:
                unique_vertices.append(vertex)
        
        # Attempt to order vertices in sequence
        if len(unique_vertices) > 2:
            # Get room type from walls
            for wall in walls:
                if wall[6] == room_id:
                    room_type = wall[5]
                    break
            
            # Set color based on room type
            color = ROOM_COLORS.get(room_type, ('#FFFFFF', 'Unknown'))[0]
            label = ROOM_COLORS.get(room_type, ('#FFFFFF', 'Unknown'))[1]
            
            # Create polygon from vertices
            try:
                # Try to create convex hull from points
                from scipy.spatial import ConvexHull
                points = np.array(unique_vertices)
                hull = ConvexHull(points)
                polygon_vertices = points[hull.vertices]
                
                # Create and add polygon
                poly = Polygon(polygon_vertices, closed=True, 
                              facecolor=color, edgecolor='black', 
                              alpha=0.8, label=label)
                plt.gca().add_patch(poly)
                
                # Add room type label in center of polygon
                centroid_x = np.mean(polygon_vertices[:, 0])
                centroid_y = np.mean(polygon_vertices[:, 1])
                
                plt.text(centroid_x, centroid_y, label,
                        horizontalalignment='center',
                        verticalalignment='center',
                        fontsize=10, fontweight='bold',
                        color='black')
            except:
                # If polygon creation fails, just plot the points
                x_coords = [v[0] for v in unique_vertices]
                y_coords = [v[1] for v in unique_vertices]
                plt.scatter(x_coords, y_coords, color=color, s=10)
    
    # Plot exterior and interior walls in solid lines
    wall_types = {14: ('black', 3, 'Exterior wall'), 
                  16: ('gray', 2, 'Interior wall')}
    
    for wall_type, (color, width, label) in wall_types.items():
        wall_plotted = False
        for wall in walls:
            if wall[5] == wall_type:
                x = [wall[0], wall[2]]
                y = [wall[1], wall[3]]
                if not wall_plotted:
                    plt.plot(x, y, color=color, linewidth=width, solid_capstyle='round', label=label)
                    wall_plotted = True
                else:
                    plt.plot(x, y, color=color, linewidth=width, solid_capstyle='round')
    
    # Plot doors in solid lines
    door_types = {15: ('brown', 3, 'Front Door'),
                  17: ('peru', 2, 'Interior Door')}
    
    for door_type, (color, width, label) in door_types.items():
        door_plotted = False
        for wall in walls:
            if wall[5] == door_type:
                x = [wall[0], wall[2]]
                y = [wall[1], wall[3]]
                if not door_plotted:
                    plt.plot(x, y, color=color, linewidth=width, solid_capstyle='round', label=label)
                    door_plotted = True
                else:
                    plt.plot(x, y, color=color, linewidth=width, solid_capstyle='round')
    
    plt.title(title)
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.gca().set_aspect('equal', adjustable='box')
    
    # Create legend without duplicates
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), 
              bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()

def visualize_all_room_types(image_path, title="All Room Types with Filled Colors", size=256, show_plot=True):
    """
    Extract and visualize all room types from both channels with filled colors.
    
    Args:
        image_path: Path to the image file
        title: Plot title
        size: Image size (default 256)
        show_plot: Whether to show the plot
    """
    # Load the image
    img = np.array(Image.open(image_path))
    
    # Extract channels
    channel_1 = img[:, :, 0]  # Wall types
    channel_2 = img[:, :, 1]  # Room types
    
    # Create a new image for visualization
    room_type_img = np.zeros_like(channel_2)
    
    # Fill with room types from channel 2
    for k in range(size):
        for h in range(size):
            # First check for exterior walls from channel 1
            if channel_1[k, h] == 127:
                room_type_img[k, h] = 14  # Exterior wall type
            # Then check room types from channel 2
            elif channel_2[k, h] in ROOM_TYPE_CONVERSION:
                room_type_img[k, h] = ROOM_TYPE_CONVERSION[channel_2[k, h]]
            # Handle special cases
            elif channel_1[k, h] == 255:
                room_type_img[k, h] = 15  # Front door
    
    if show_plot:
        # Create a colormap for room types
        unique_types = np.unique(room_type_img)
        colors = [ROOM_COLORS.get(i, ('#FFFFFF', 'Unknown'))[0] for i in range(max(unique_types) + 1)]
        cmap = mcolors.ListedColormap(colors)
        
        plt.figure(figsize=(15, 10))
        plt.imshow(room_type_img, cmap=cmap)
        
        # Create legend
        legend_elements = [plt.Rectangle((0, 0), 1, 1, facecolor=ROOM_COLORS.get(i, ('#FFFFFF', 'Unknown'))[0], 
                                       label=ROOM_COLORS.get(i, ('#FFFFFF', 'Unknown'))[1]) 
                          for i in unique_types if i in ROOM_COLORS]
        
        plt.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    return room_type_img

def visualize_floorplan_with_all_room_types(image_path, title="Complete Floor Plan with All Room Types", include_walls=True):
    """
    Visualize the floor plan with all room types from both channels and vector-based walls.
    
    Args:
        image_path: Path to the image file
        title: Plot title
        include_walls: Whether to include wall lines on top of the filled colors
    """
    from PIL import Image
    from read_dd import read_data
    
    # Load the image
    img = np.array(Image.open(image_path))
    
    # Get the room type image
    room_type_img = visualize_all_room_types(image_path, show_plot=False)
    
    # Process the data to get walls and doors
    rm_type, poly, doors, walls, out = read_data(image_path)
    
    if include_walls:
        # Plot walls and doors on top
        visualize_filled_floorplan(rm_type, walls, doors, title=title)
    
    return room_type_img, walls, doors

def visualize_combined_floorplan(image_path, title="Combined Room Types with Filled Colors", show_walls=True):
    """
    Visualize all room types from channel 2 and exterior walls from channel 1,
    with filled colors for each room type.
    
    Args:
        image_path: Path to the image file
        title: Plot title
        show_walls: Whether to show vector walls overlaid on the filled colors
    """
    from PIL import Image
    from read_dd import read_data
    
    # Load the image
    img = np.array(Image.open(image_path))
    size = img.shape[0]
    
    # Process data - this will extract all information including walls
    rm_type, poly, doors, walls, out = read_data(image_path)
    
    # Create a new visualization
    plt.figure(figsize=(15, 10))
    
    # Group walls by room ID (wall[6]) and room type (wall[5])
    rooms_by_id = {}
    for wall in walls:
        room_id = wall[6]
        room_type = wall[5]
        
        # Create a key combining room_id and room_type to differentiate walls
        key = (room_id, room_type)
        
        if key not in rooms_by_id:
            rooms_by_id[key] = []
        
        # Add vertices
        rooms_by_id[key].append((wall[0], wall[1]))
        rooms_by_id[key].append((wall[2], wall[3]))
    
    # Create a background filled with exterior walls (if needed)
    if any(key[1] == 14 for key in rooms_by_id):
        # Create a blank background
        background = np.ones((size, size, 3))
        bg_color = np.array(mcolors.to_rgb(ROOM_COLORS.get(14, ('#FFFFFF'))[0]))
        background[:, :] = bg_color
        plt.imshow(background, extent=(0, size, 0, size))
    
    # Plot each room as a filled polygon
    for key, vertices in rooms_by_id.items():
        room_id, room_type = key
        
        # Skip walls and doors if they're not part of rooms
        if room_type in [16, 17]:
            continue
            
        # Find unique vertices to create polygon
        unique_vertices = []
        for vertex in vertices:
            if vertex not in unique_vertices:
                unique_vertices.append(vertex)
        
        if len(unique_vertices) > 2:
            # Set color based on room type
            color = ROOM_COLORS.get(room_type, ('#FFFFFF', 'Unknown'))[0]
            label = ROOM_COLORS.get(room_type, ('#FFFFFF', 'Unknown'))[1]
            
            try:
                # Try to create convex hull from points
                from scipy.spatial import ConvexHull
                points = np.array(unique_vertices)
                hull = ConvexHull(points)
                polygon_vertices = points[hull.vertices]
                
                # Create and add polygon
                poly = Polygon(polygon_vertices, closed=True, 
                              facecolor=color, edgecolor=None if not show_walls else 'black', 
                              alpha=0.9, label=label)
                plt.gca().add_patch(poly)
                
                # Add room type label in center of polygon
                centroid_x = np.mean(polygon_vertices[:, 0])
                centroid_y = np.mean(polygon_vertices[:, 1])
                
                plt.text(centroid_x, centroid_y, label,
                        horizontalalignment='center',
                        verticalalignment='center',
                        fontsize=10, fontweight='bold',
                        color='black')
            except:
                # If polygon creation fails, use a different approach
                # Just fill in the room area from the image data
                room_type_from_img = None
                for typ in rm_type:
                    if typ == room_type:
                        room_type_from_img = typ
                        break
                
                if room_type_from_img is not None:
                    # This is a fallback that just marks the area with points
                    x_coords = [v[0] for v in unique_vertices]
                    y_coords = [v[1] for v in unique_vertices]
                    plt.scatter(x_coords, y_coords, color=color, s=5, label=label)
    
    # If showing walls, plot them on top
    if show_walls:
        # Plot exterior and interior walls in solid lines
        wall_types = {
            14: ('black', 2, 'Exterior wall'), 
            16: ('dimgray', 1.5, 'Interior wall'),
            15: ('saddlebrown', 2, 'Front Door'),
            17: ('peru', 1.5, 'Interior Door')
        }
        
        # Plot all wall types
        for wall_type, (color, width, label) in wall_types.items():
            wall_plotted = False
            for wall in walls:
                if wall[5] == wall_type:
                    x = [wall[0], wall[2]]
                    y = [wall[1], wall[3]]
                    if not wall_plotted:
                        plt.plot(x, y, color=color, linewidth=width, solid_capstyle='round', label=label)
                        wall_plotted = True
                    else:
                        plt.plot(x, y, color=color, linewidth=width, solid_capstyle='round')
    
    plt.title(title)
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.gca().set_aspect('equal', adjustable='box')
    
    # Create legend without duplicates
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), 
              bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()
    
    return rm_type, walls, doors

def visualize_extracted_data(rm_type, poly, doors, walls, title="Floor Plan from Extracted Data", size=256, show_labels=True):
    """
    Visualize the floor plan using only the extracted data from read_data.
    Uses filled colors for rooms and simple solid lines for walls.
    
    Args:
        rm_type: List of room types (from read_data)
        poly: List of polygon vertex counts (from read_data)
        doors: List of door coordinates (from read_data)
        walls: List of wall coordinates and types (from read_data)
        title: Plot title
        size: Image size (default 256)
        show_labels: Whether to show room type labels
    """
    plt.figure(figsize=(15, 10))
    
    # Create a white background
    plt.fill([0, size, size, 0], [0, 0, size, size], 'white')
    
    # Group walls by room id (index 6 in wall data)
    walls_by_room = {}
    
    # First, collect all walls that form room boundaries (not doors or walls)
    for wall in walls:
        room_id = wall[6]
        wall_type = wall[5]
        
        # Skip walls and doors
        if wall_type in [14, 15, 16, 17]:
            continue
            
        # Add to the room dictionary
        if room_id not in walls_by_room:
            walls_by_room[room_id] = []
            
        # Store wall segments
        walls_by_room[room_id].append((
            (wall[0], wall[1]),  # start point
            (wall[2], wall[3]),  # end point
            wall_type            # room type
        ))
    
    # Function to order wall segments to form a closed polygon
    def order_wall_segments(walls):
        if not walls:
            return []
            
        ordered_points = []
        remaining_walls = walls.copy()
        
        # Start with the first wall
        current_wall = remaining_walls.pop(0)
        ordered_points.append(current_wall[0])
        ordered_points.append(current_wall[1])
        current_point = current_wall[1]
        
        # Connect walls until we form a closed loop
        max_iterations = len(remaining_walls) * 2  # Prevent infinite loops
        iteration = 0
        
        while remaining_walls and iteration < max_iterations:
            iteration += 1
            found = False
            
            # Find the next connected wall
            for i, wall in enumerate(remaining_walls):
                # Check if wall starts at current point
                if np.linalg.norm(np.array(wall[0]) - np.array(current_point)) < 1.0:
                    ordered_points.append(wall[1])
                    current_point = wall[1]
                    remaining_walls.pop(i)
                    found = True
                    break
                # Check if wall ends at current point
                elif np.linalg.norm(np.array(wall[1]) - np.array(current_point)) < 1.0:
                    ordered_points.append(wall[0])
                    current_point = wall[0]
                    remaining_walls.pop(i)
                    found = True
                    break
            
            # If we can't find a connected wall, try the next wall
            if not found and remaining_walls:
                current_wall = remaining_walls.pop(0)
                ordered_points.append(current_wall[0])
                ordered_points.append(current_wall[1])
                current_point = current_wall[1]
        
        return ordered_points
    
    # Draw each room
    for room_id, room_walls in walls_by_room.items():
        # Get the room type from the first wall segment
        room_type = room_walls[0][2]
        
        # Get the room color and label
        color = ROOM_COLORS.get(room_type, ('#FFFFFF', 'Unknown'))[0]
        label = ROOM_COLORS.get(room_type, ('#FFFFFF', 'Unknown'))[1]
        
        # Order wall segments to form a closed polygon
        ordered_points = order_wall_segments(room_walls)
        
        if len(ordered_points) >= 3:  # Need at least 3 points for a polygon
            # Create polygon
            polygon = Polygon(ordered_points, closed=True, 
                            facecolor=color, edgecolor='none', 
                            alpha=0.9, label=label)
            plt.gca().add_patch(polygon)
            
            # Add room label if requested
            if show_labels:
                # Calculate the centroid of the room
                x_coords = [p[0] for p in ordered_points]
                y_coords = [p[1] for p in ordered_points]
                centroid_x = sum(x_coords) / len(x_coords)
                centroid_y = sum(y_coords) / len(y_coords)
                
                plt.text(centroid_x, centroid_y, label,
                        horizontalalignment='center',
                        verticalalignment='center',
                        fontsize=10, fontweight='bold',
                        color='black')
    
    # Draw all walls
    for wall in walls:
        x = [wall[0], wall[2]]
        y = [wall[1], wall[3]]
        wall_type = wall[5]
        
        # Choose line color and width based on wall type
        if wall_type == 14:  # Exterior wall
            color = 'black'
            width = 2
        elif wall_type == 16:  # Interior wall
            color = 'gray'
            width = 1.5
        elif wall_type in [15, 17]:  # Doors
            color = 'saddlebrown'
            width = 2
        else:
            continue
            
        # Draw the wall
        plt.plot(x, y, color=color, linewidth=width, solid_capstyle='round')
    
    # Set plot properties
    plt.title(title)
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.gca().set_aspect('equal', adjustable='box')
    
    # Create legend without duplicates
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), 
              bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()
    
    return

# Example usage:
"""
from visualize import visualize_combined_floorplan

# This will extract all information and visualize it with filled colors
image_path = "image/291.png"  # Your image path
rm_type, walls, doors = visualize_combined_floorplan(image_path)
""" 