import numpy as np 
from PIL import Image
import mask_to_poly as mr

# Define the mappings for each channel
CHANNEL_1_MAPPING = {
    127: "Exterior wall",
    255: "Front door",
    0: "Other"
}

CHANNEL_2_MAPPING = {
    0: "Living room",
    1: "Master room",
    2: "Kitchen",
    3: "Bathroom",
    4: "Dining room",
    5: "Child room",
    6: "Study room",
    7: "Second room",
    8: "Guest room",
    9: "Balcony",
    10: "Entrance",
    11: "Storage",
    12: "Wall-in",
    13: "External area",
    14: "Exterior wall",
    15: "Front door",
    16: "Interior wall",
    17: "Interior door"
}

# Room type conversion mapping (from channel 2 values to final room type numbers)
ROOM_TYPE_CONVERSION = {
    0: 1,   # Living room -> 1
    1: 3,   # Master room -> 3
    2: 2,   # Kitchen -> 2
    3: 4,   # Bathroom -> 4
    4: 7,   # Dining room -> 7
    5: 3,   # Child room -> 3 (bedroom)
    6: 8,   # Study room -> 8
    7: 3,   # Second room -> 3 (bedroom)
    8: 3,   # Guest room -> 3 (bedroom)
    9: 5,   # Balcony -> 5
    10: 6,  # Entrance -> 6
    11: 10, # Storage -> 10
    14: 14, # Exterior wall -> 14
    15: 15, # Front door -> 15
    16: 16, # Interior wall -> 16
    17: 17  # Interior door -> 17
}

def read_door(door_img,img,tmp_diff):
	tmp3=door_img.copy()
	tmp4=door_img.copy()
	for k in range(256):
		for h in range(256):
			has=[]
			for knm in range(10):
				has.append(0)
			if(tmp4[k][h]==1):
				p=img[k-tmp_diff-4:k+tmp_diff+4,h-tmp_diff-4:h+tmp_diff+4,2]
				s=p[np.nonzero(p)]
				if(len(s)==0):
					continue
				r=[]
				kmmmm=s[0]
				for t in range(len(s)):
					if(t==0):
						r.append(s[t])
					elif(s[t] not in r):
						r.append(s[t])
				if(len(r)>=3):
					tmp3[k][h]=0	
				elif(len(r)==2):
					has[r[0]]=1
					has[r[1]]=1
					tmp3[k][h]= has[0]*1+has[1]*2+has[3]*4+has[4]*8+has[5]*16+has[6]*32+has[7]*64+has[8]*128+has[9]*256
	s=np.unique(tmp3)
	tmp4=tmp3.copy()
	for ks in range(len(s)):
		for k in range(256):
			for h in range(256):
				if(tmp3[k][h]==s[ks]):
					tmp4[k][h]=int(ks)
	return tmp4


def sort_corners(corners ,k_d):
	coords=[]
	ind=[]
	if(k_d==0):
		for j in range(len(corners)):
			ind.append(0)
		for i in range(len(corners)):
			if (i==0):
				coords.append(corners[0])
				ind[i]=1

			elif(i%2==1):
				k=coords[i-1][0]
				for j in range(len(corners)):
					if(corners[j][0]==k)& ( ind[j]!=1):
						coords.append(corners[j])
						ind[j]=1
						break
			elif(i%2==0):
				k=coords[i-1][1]
				for j in range(len(corners)):
					if(corners[j][1]==k)&  (ind[j]!=1):
						coords.append(corners[j])
						ind[j]=1
						break
					
	if(k_d==1):
		for s in range(len(corners)):
			ind.append(0)
		p=0		
		for i in range(len(corners)):
			if (i%4==0):
				coords.append(corners[i])
				ind[i]=1
				p=p+1
			elif(i%2==1):
				k=coords[i-1][0]
				tk=coords[i-1][1]  
				pp=0
				for j in range(len(corners)):
					if(corners[j][0]==k)& (ind[j]!=1):
						if(pp==0) :
							pp=pp+1
							coords.append(corners[j])
							fn=j
						else:
							if (abs(corners[j][1]-tk)<=abs(coords[i][1]-tk)) &(abs(corners[j][1]-tk)!=0):
								coords[i]=corners[j]
								fn=j
				ind[fn]=ind[fn]+1
				fn=-1		
				p=p+1
			elif(i%2==0)& (i%4!=0):
				p=p+1
				k=coords[i-1][1]
				tk=coords[i-1][0] 
				pp=0
				for j in range(len(corners)):
					if(corners[j][1]==k) & (ind[j]!=1):
						if(pp==0):
							pp=pp+1
							coords.append(corners[j])
							fn=j  						
						else:
							if (abs(corners[j][0]-tk)<=abs(coords[i][0]-tk)) &(abs(corners[j][0]-tk)!=0):
								coords[i]=corners[j]
								fn=j  
				ind[fn]=ind[fn]+1 
				fn=-1
	return coords
			
def read_data(line):
	poly=[]
	img = np.asarray(Image.open(line))
	dec=0
	
	# Extract channels
	img_wall_types = img[:,:,0]    # Channel 1: Wall types
	img_room_types = img[:,:,1]    # Channel 2: Room types
	img_room_numbers = img[:,:,2]  # Channel 3: Room numbers
	
	# Initialize wall image
	wall_img = np.zeros((256, 256))
	
	# Process wall types from both channels
	for k in range(256):
		for h in range(256):
			# Channel 1 wall types
			if img_wall_types[k][h] == 127:  # Exterior wall
				wall_img[k][h] = 14
			elif img_wall_types[k][h] == 255:  # Front door
				wall_img[k][h] = 15
			# Channel 2 wall types
			elif img_room_types[k][h] == 16:  # Interior wall
				wall_img[k][h] = 16
			elif img_room_types[k][h] == 17:  # Interior door
				wall_img[k][h] = 17
	
	# Process rooms
	room_no = img_room_numbers.max()
	room_imgs = []
	rm_types = []
	
	for i in range(room_no):
		room_img = np.zeros((256, 256))
		for k in range(256):
			for h in range(256):
				if img_room_numbers[k][h] == i+1:
					room_img[k][h] = 1
					k_ = k
					h_ = h
		
		# Get room type from channel 2
		rm_t = img_room_types[k_][h_]
		
		# Convert room type using the mapping
		if rm_t in ROOM_TYPE_CONVERSION:
			rm_types.append(ROOM_TYPE_CONVERSION[rm_t])
		else:
			# Handle special cases from channel 1
			if img_wall_types[k_][h_] == 127:
				rm_types.append(14)  # Exterior wall
			else:
				rm_types.append(16)  # Unknown/Interior wall
		
		room_imgs.append(room_img)

	# Process walls and doors
	walls = []
	doors = []
	windows = []  # New list to store window coordinates
	rm_type = rm_types
	
	# Process each room's walls
	for t in range(len(room_imgs)):
		tmp = room_imgs[t]
		# Fill small gaps in walls
		for k in range(254):
			for h in range(254):
				if(tmp[k][h]==1) & (tmp[k+1][h]==0) & (tmp[k+2][h]==1):
					tmp[k+1][h] = 1
				if(tmp[h][k]==1) & (tmp[h][k+1]==0) & (tmp[h][k+2]==1):
					tmp[h][k+1] = 1
				if(tmp[k][h]==0) & (tmp[k+1][h]==1) & (tmp[k+2][h]==0):
					tmp[k+1][h] = 0
				if(tmp[h][k]==0) & (tmp[h][k+1]==1) & (tmp[h][k+2]==0):
					tmp[h][k+1] = 0

		room_imgs[t] = tmp
		poly2 = mr.get_polygon(room_imgs[t])
		coords_1 = list(poly2.exterior.coords)
		coords = []
		for kn in range(len(coords_1)):
			coords.append([list(coords_1[kn])[1], list(coords_1[kn])[0], 0, 0, t, rm_type[t]])
		
		for c in range(len(coords)-1):
			walls.append([coords[c][0], coords[c][1], coords[c+1][0], coords[c+1][1], -1, coords[c][5], coords[c][4], -1, 0])
		poly.append(len(coords)-1)

	# Process interior doors (from channel 2)
	door_img = np.zeros((256, 256))
	for k in range(256):
		for h in range(256):
			if img_room_types[k][h] == 17:  # Interior door from channel 2
				door_img[k][h] = 1
	
	# Find door corners and calculate tmp_diff
	tmp = door_img.copy()
	coords = []
	for k in range(2, 254):
		for h in range(2, 254):
			if tmp[k][h] == 1:
				if ((tmp[k-1][h]==0) & (tmp[k-1][h-1]==0) & (tmp[k][h-1]==0)):
					coords.append([h, k, 0, 0])
				elif (tmp[k+1][h]==0) & (tmp[k+1][h-1]==0) & (tmp[k][h-1]==0):
					coords.append([h, k, 0, 0])
				elif (tmp[k+1][h]==0) & (tmp[k+1][h+1]==0) & (tmp[k][h+1]==0): 
					coords.append([h, k, 0, 0])
				elif (tmp[k-1][h]==0) & (tmp[k-1][h+1]==0) & (tmp[k][h+1]==0): 
					coords.append([h, k, 0, 0])					
				elif (tmp[k+1][h]==1) & (tmp[k][h+1]==1) & (tmp[k+1][h+1]==0):
					coords.append([h, k, 0, 0])					
				elif (tmp[k-1][h]==1) & (tmp[k][h+1]==1) & (tmp[k-1][h+1]==0):
					coords.append([h, k, 0, 0])					
				elif (tmp[k+1][h]==1) & (tmp[k][h-1]==1) & (tmp[k+1][h-1]==0): 
					coords.append([h, k, 0, 0])				
				elif (tmp[k-1][h]==1) & (tmp[k][h-1]==1) & (tmp[k-1][h-1]==0):
					coords.append([h, k, 0, 0])
	
	# Calculate tmp_diff (minimum non-trivial distance between points)
	tmp_diff = 1000000
	if len(coords) > 0:
		p_x_1 = coords[0][0]
		for k in range(1, len(coords)):
			p_x_2 = coords[k][0]
			tmp_dif = abs(p_x_1 - p_x_2)
			if (tmp_dif < tmp_diff) & (tmp_dif > 1):
				tmp_diff = tmp_dif
		
		p_y_1 = coords[0][1]
		for k in range(1, len(coords)):
			p_y_2 = coords[k][1]
			tmp_dif = abs(p_y_1 - p_y_2)
			if (tmp_dif < tmp_diff) & (tmp_dif > 1):
				tmp_diff = tmp_dif
	else:
		# Default value if no door corners are found
		tmp_diff = 4
	
	# Process door regions
	door_imgs = read_door(door_img, img, tmp_diff)
	door_no = int(door_imgs.max())
	doors_img = []
	
	for i in range(door_no):
		door_img = np.zeros((256, 256))
		for k in range(256):
			for h in range(256):
				if door_imgs[k][h] == i+1:
					door_img[k][h] = 1
		doors_img.append(door_img)
	
	rmpn = len(doors_img)
	
	# Process each door region
	for t in range(len(doors_img)):
		tmp = doors_img[t]
		if np.max(tmp) <= 0:
			dec += 1
			continue
			
		poly2 = mr.get_polygon(doors_img[t])
		coords_1 = list(poly2.exterior.coords)
		coords = []
		for kn in range(len(coords_1)):
			coords.append([list(coords_1[kn])[1], list(coords_1[kn])[0], 0, 0, t, 17])
			
		for c in range(len(coords)-1):
			walls.append([coords[c][0], coords[c][1], coords[c+1][0], coords[c+1][1], -1, 17, len(rm_type)+coords[c][4]-dec, -1, 0])
			doors.append([coords[c][0], coords[c][1], coords[c+1][0], coords[c+1][1]])
		poly.append(len(coords)-1)

	# Process front doors (from channel 1)
	frontdoor_img = np.zeros((256, 256))
	for k in range(256):
		for h in range(256):
			if img_wall_types[k][h] == 255:  # Front door from channel 1
				frontdoor_img[k][h] = 1
	
	if np.max(frontdoor_img) > 0:
		poly2 = mr.get_polygon(frontdoor_img)
		coords_1 = list(poly2.exterior.coords)
		coords = []
		for kn in range(len(coords_1)):
			coords.append([list(coords_1[kn])[1], list(coords_1[kn])[0], 0, 0, 0, 15])
		
		for c in range(len(coords)-1):
			walls.append([coords[c][0], coords[c][1], coords[c+1][0], coords[c+1][1], -1, 15, rmpn+len(rm_type)+2, -1, 0])
			doors.append([coords[c][0], coords[c][1], coords[c+1][0], coords[c+1][1]])
		poly.append(len(coords)-1)
	
	# Process exterior walls (from channel 1)
	exterior_img = np.zeros((256, 256))
	for k in range(256):
		for h in range(256):
			if img_wall_types[k][h] == 127:  # Exterior wall from channel 1
				exterior_img[k][h] = 1
	
	if np.max(exterior_img) > 0:
		poly2 = mr.get_polygon(exterior_img)
		coords_1 = list(poly2.exterior.coords)
		coords = []
		for kn in range(len(coords_1)):
			coords.append([list(coords_1[kn])[1], list(coords_1[kn])[0], 0, 0, 0, 14])
		
		for c in range(len(coords)-1):
			walls.append([coords[c][0], coords[c][1], coords[c+1][0], coords[c+1][1], -1, 14, rmpn+len(rm_type)+1, -1, 0])
		poly.append(len(coords)-1)
		if 14 not in rm_type:
			rm_type.append(14)
	
	# Update room types with doors
	no_doors = int(len(doors)/4)
	for i in range(no_doors-1):
		rm_type.append(17)  # Interior doors
	if no_doors > 0:
		rm_type.append(15)  # Front door
	
	# Detect windows on exterior walls
	# Create a potential window wall type ID (18)
	window_wall_type = 18
	
	# Collect all exterior walls
	exterior_walls = []
	for wall in walls:
		if wall[5] == 14:  # Exterior wall
			exterior_walls.append(wall)
	
	# Find exterior walls that border rooms
	for ext_wall in exterior_walls:
		x1, y1, x2, y2 = ext_wall[0], ext_wall[1], ext_wall[2], ext_wall[3]
		
		# Calculate wall length
		wall_length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
		
		# Only consider walls of sufficient length for windows (min 10 pixels)
		if wall_length < 10:
			continue
		
		# Get points along the wall to check for adjacent rooms
		# We'll sample several points along the wall
		samples = 5
		has_room_adjacent = False
		
		for i in range(samples):
			# Calculate point along the wall
			t = (i + 1) / (samples + 1)  # interpolation factor 
			x = int(x1 + t * (x2 - x1))
			y = int(y1 + t * (y2 - y1))
			
			# Calculate normal vector to the wall (perpendicular)
			dx = x2 - x1
			dy = y2 - y1
			length = np.sqrt(dx*dx + dy*dy)
			
			if length == 0:
				continue
				
			# Normalize and create perpendicular vector (rotate 90 degrees)
			nx, ny = -dy/length, dx/length  # Outward normal
			
			# Check points in both directions from the wall
			for direction in [-1, 1]:
				# Check a point 3 pixels away from the wall
				check_x = int(x + direction * 3 * nx)
				check_y = int(y + direction * 3 * ny)
				
				# Make sure we're inside the image bounds
				if 0 <= check_x < 256 and 0 <= check_y < 256:
					# If this point is inside a room (not wall, not outside)
					room_number = img_room_numbers[check_y, check_x]
					if room_number > 0:
						has_room_adjacent = True
						break
			
			if has_room_adjacent:
				break
		
		# If wall has a room adjacent, add window
		if has_room_adjacent:
			# Window midpoint
			mid_x = (x1 + x2) / 2
			mid_y = (y1 + y2) / 2
			
			# Get wall direction
			wall_dir_x = (x2 - x1) / wall_length
			wall_dir_y = (y2 - y1) / wall_length
			
			# Create window segment (approximately 1/4 of the wall length)
			window_length = wall_length / 4
			window_x1 = mid_x - window_length/2 * wall_dir_x
			window_y1 = mid_y - window_length/2 * wall_dir_y
			window_x2 = mid_x + window_length/2 * wall_dir_x
			window_y2 = mid_y + window_length/2 * wall_dir_y
			
			windows.append([window_x1, window_y1, window_x2, window_y2])
	
	# Validate output
	out = 1
	for i in range(len(poly)):
		if poly[i] < 4:
			out = -1
	if len(doors) % 4 != 0:
		out = -3
	
	assert out == 1, f"Error in reading the file {line}, {out=} but expected out==1"
	return rm_type, poly, doors, walls, windows, out
	
