
import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from bossroom import generate_dnd_boss_room_layout_v8  # Assuming this is a custom module you've created

# Define the dimensions of the grid
width, height = 30, 30

# Create an empty grid filled with -1 as placeholders
grid = [[-1 for x in range(width)] for y in range(height)]

# Function to check if a circular area around a point is empty
def is_circle_empty(grid, center_x, center_y, radius):
    # Check if all cells within the circular area are empty (-1)
    for i in range(-radius, radius+1):
        for j in range(-radius, radius+1):
            if (i**2 + j**2 <= radius**2) and (center_y + j >= height or center_y + j < 0 or center_x + i >= width or center_x + i < 0 or grid[center_y + j][center_x + i] != -1):
                return False
    return True

# Function to create a random room of a given shape (rectangle or circle)
def create_random_room(grid, shape=None, max_attempts=1000):
    # If shape is not specified, randomly choose between rectangle and circle
    if not shape:
        shape = random.choice(['rectangle', 'circle'])

    for _ in range(max_attempts):
        if shape == 'rectangle':
            # Define room dimensions and position
            room_width = random.randint(3, 6)
            room_height = random.randint(3, 6)
            room_x = random.randint(0, width - room_width - 1)
            room_y = random.randint(0, height - room_height - 1)
            
            # Check if all cells within the rectangle are empty
            if all(grid[room_y + j][room_x + i] == -1 for i in range(room_width) for j in range(room_height)):
                # Fill the room with 0s to represent it
                for i in range(room_width):
                    for j in range(room_height):
                        grid[room_y + j][room_x + i] = 0
                return room_x, room_y, room_width, room_height, ""

        elif shape == 'circle':
            # Define room radius and position
            radius = random.randint(2, 4)
            room_x = random.randint(radius, width - radius - 1)
            room_y = random.randint(radius, height - radius - 1)

            # Check if the circular area around the room is empty
            if is_circle_empty(grid, room_x, room_y, radius):
                # Fill the circular area with 0s to represent it
                for i in range(-radius, radius+1):
                    for j in range(-radius, radius+1):
                        if i**2 + j**2 <= radius**2:
                            grid[room_y + j][room_x + i] = 0
                return room_x - radius, room_y - radius, 2*radius, 2*radius, ""

    return None

# Function to connect two rooms by creating a path between their centers
def connect_rooms(grid, room1, room2):
    x1, y1 = room1[0] + room1[2] // 2, room1[1] + room1[3] // 2
    x2, y2 = room2[0] + room2[2] // 2, room2[1] + room2[3] // 2

    while (x1, y1) != (x2, y2):
        if x1 < x2:
            grid[y1][x1] = 1
            x1 += 1
        elif x1 > x2:
            grid[y1][x1] = 1
            x1 -= 1
        elif y1 < y2:
            grid[y1][x1] = 1
            y1 += 1
        else:
            grid[y1][x1] = 1
            y1 -= 1

# Function to determine the type of room based on its grid coordinates
def determine_room_type(x, y):
    # Placeholder logic for determining room type (you can customize this)
    if grid[y][x] == 0:
        return 'Regular'
    elif grid[y][x] == 1:
        return 'Path'
    else:
        return 'Wall'

# Function to create grouped rooms with specified labels, shapes, and caption chances
def create_grouped_rooms(grid, labels, shapes, max_attempts=1000, caption_chance=None):
    assert len(labels) == len(shapes), "Labels and shapes arrays should have the same length."
    if not caption_chance:
        caption_chance = [1.0] * len(labels)
    assert len(labels) == len(caption_chance), "Labels and caption_chance arrays should have the same length."

    grouped_rooms = []
    for idx, shape in enumerate(shapes):
        for _ in range(max_attempts):
            room = create_random_room(grid, shape)
            if room:
                room = list(room)
                room[-1] = labels[idx] if random.random() < caption_chance[idx] else ""
                grouped_rooms.append(tuple(room))
                break
    return grouped_rooms

# Function to connect grouped rooms in a sequence
def connect_grouped_rooms(grid, grouped_rooms):
    for i in range(len(grouped_rooms) - 1):
        connect_rooms(grid, grouped_rooms[i], grouped_rooms[i + 1])

# Function to find the nearest room to a given room within a list of rooms
def find_nearest_room(src_room, rooms_list):
    min_distance = float('inf')
    nearest_room = None
    src_center_x, src_center_y = src_room[0] + src_room[2] // 2, src_room[1] + src_room[3] // 2

    for room in rooms_list:
        dest_center_x, dest_center_y = room[0] + room[2] // 2, room[1] + room[3] // 2
        distance = (src_center_x - dest_center_x)**2 + (src_center_y - dest_center_y)**2
        if distance < min_distance:
            min_distance = distance
            nearest_room = room

    return nearest_room

# Colors and colormap for room visualization
colors = np.array([


    [0, 0, 0],     # Black for walls (-1)
    [1, 0.6, 0.8], # Pink for rooms (0)
    [1, 1, 1],     # White for paths (1)
])
cmap = ListedColormap(colors)

# Define group parameters - labels and shapes for each group
group_params = [
    (['Treasure', 'Puzzle'], ['rectangle', 'rectangle'], [0.6, 1.0]),
    (['Treasure', 'Strong Monsters'], ['rectangle', 'circle'], [0.2, 0.6]),
    (['Trap'], ['rectangle'], [0.7]),
    (['Boss', "Treasure"], ['rectangle', 'circle'], [0.8, 0.6]),
    (['NPC'], ['rectangle'], [0.7]),
]

# Define parameters for rooms that are guaranteed to be included
guaranteed_rooms_params = [
    ('Boss', 'circle'),
    ('Entrance', 'rectangle'),
]

# Initialize lists for rooms without captions and unused guaranteed labels
rooms_without_captions = []
guaranteed_rooms = []

# Create rooms for guaranteed parameters
for label, shape in guaranteed_rooms_params:
    room = create_random_room(grid, shape)
    if room:
        room = list(room)
        room[-1] = label
        guaranteed_rooms.append(tuple(room))

# Update unused guaranteed labels
unused_guaranteed_labels = [label for label, shape in guaranteed_rooms_params]

# Update rooms without captions
for room in guaranteed_rooms:
    if room[4] in unused_guaranteed_labels:
        unused_guaranteed_labels.remove(room[4])

# Generate and connect rooms for each group
all_groups = []
for params in group_params:
    labels, shapes, chances = params
    group = create_grouped_rooms(grid, labels, shapes, caption_chance=chances)
    connect_grouped_rooms(grid, group)
    all_groups.append(group)
    for room in group:
        if not room[4]:
            rooms_without_captions.append(room)

# Connect groups together
for i in range(len(all_groups) - 1):
    connect_rooms(grid, all_groups[i][-1], all_groups[i + 1][0])

# Connect guaranteed rooms to their nearest neighbors
for g_room in guaranteed_rooms:
    nearest = find_nearest_room(g_room, [r for group in all_groups for r in group])
    connect_rooms(grid, g_room, nearest)

# Assign unused guaranteed labels to rooms without captions
print("Unused labels before assignment:", unused_guaranteed_labels)
default_labels = ["Monster", "Treasure", "Secret Boss"]
for room in rooms_without_captions:
    if default_labels:
        room_caption = default_labels.pop(0)
        for group in all_groups:
            if room in group:
                idx = group.index(room)
                room_as_list = list(group[idx])
                room_as_list[4] = room_caption
                group[idx] = tuple(room_as_list)
                break

# Determine room type and add descriptions for each room type
for y in range(height):
    for x in range(width):
        # Determine the type of room based on your criteria
        room_type = determine_room_type(x, y)  # Placeholder for your room type determination logic

        if room_type == 'Boss':
            # Generate a separate map for the boss room using the function from map6.py
            boss_room_layout = generate_dnd_boss_room_layout_v8(4)
            # Optionally, you can do something with boss_room_layout, like saving it

print("Unused labels after assignment:", unused_guaranteed_labels)

# Check for rooms that still don't have captions assigned
rooms_still_without_captions = [room for group in all_groups for room in group if not room[4]]
print("Rooms without captions after assignment:", rooms_still_without_captions)

# Room descriptions for various room types
room_descriptions = {
    'Treasure': [
        'Gemstone in a Cursed Chest: Treasure: A fire opal gemstone, glowing with an inner light, valued at around 500 gold pieces. Trap: The chest is rigged with an explosive rune that detonates upon incorrect handling. Trap Damage: 4d8 fire damage. DC Check: DC 15 Intelligence (Arcana) to disarm the rune.',
        # Add more descriptions for the 'Treasure' room type
    ],
    'NPC': [
        'Eldon, the Wandering Merchant, He sells magical items, potions, and sometimes information ',
        # Add more descriptions for the 'NPC' room type
    ],
    'Puzzle': [
        'Riddle: "I fly without wings, I cry without eyes. Whenever I go, darkness flies. What am I?" Answer: A cloud.',
        # Add more descriptions for the 'Puzzle' room type
    ],
    'Boss': [
        'The Gloomdeep Caverns: A pair of Umber Hulks (CR 4 each), 200 gold pieces, a Potion of Greater Healing',
        # Add more descriptions for the 'Boss' room type
    ],
    'Entrance': [
        'Entrance to the dungeon - your adventure starts here!',
        # Add more descriptions for the 'Entrance' room type
    ],
    'Monster': [
        'The Cursed Library: Encounter: A Specter (CR 1) and a pair of Animated Armors (CR 1 each). Loot: 50-100 gold pieces, a scroll of a random 1st or 2nd-level spell',
        # Add more descriptions for the 'Monster' room type
    ],
    'Strong Monsters': [
        'The Elemental Rift: A Lesser Air Elemental (CR 4), Wind Fan, an elemental gem (air)',
        # Add more descriptions for the 'Strong Monsters' room type
    ],
    'Secret Boss': [
        'Ancient Dragons Lair: Monster: Young Red Dragon (CR 6) Loot: Dragon scales suitable for high-quality armor crafting, a Fire Resistance Ring, and a treasure hoard containing 2000 gold pieces and several precious gemstones.',
        # Add more descriptions for the 'Secret Boss' room type
    ],
    'Trap': [
        'Arcane Rune Trap: Description: A magical rune on the floor that activates when stepped on. Effect: Releases a burst of lightning energy, dealing 4d10 lightning damage (DC 15 Dexterity saving throw for half damage). Trigger: Stepping on the rune.',
        # Add more descriptions for the 'Trap' room type
    ],
}

# Create a set to store unique captions
captions = set()
for group in all_groups:
    for room in group:
        if room[4]:  # Check if the room has a caption
            captions.add(room[4])  # Add the caption to the set
            # Get the center coordinates of the room for labeling on the map
            room_center_x, room_center_y = room[0] + room[2] // 2, room[1] + room[3] // 2
            # Display the room caption on the map
            plt.text(room_center_x, room_center_y, room[4], ha='center', va='center', color='black', fontsize=9)

# Iterate through each caption (room label) in the 'captions' set
for caption in captions:
    # Retrieve the room descriptions for the current caption from 'room_descriptions' dictionary
    descriptions = room_descriptions.get(caption, "No description available.")
    
    # Check if descriptions is a list (multiple descriptions available for the room)
    if isinstance(descriptions, list):
        # Randomly select one description from the list
        description = random.choice(descriptions)
    else:
        # Use the single description if it's not a list
        description = descriptions
    
    # Create an empty plot element (used for legend)
    plt.plot([], [], ' ', label=f"{caption}: {description}")

# Add a legend to the plot with room labels and their descriptions
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Room Descriptions", fontsize='small')

# Calculate and print the total number of rooms generated on the grid
total_rooms_generated = len(guaranteed_rooms) + sum(len(group) for group in all_groups)
print("Total rooms generated:", total_rooms_generated)

# Calculate and print the total number of empty rooms (rooms with value 0) on the grid
print("Total rooms in grid:", sum(1 for row in grid for cell in row if cell == 0))

# Display the grid as an image, specifying the colormap, origin, and value range
plt.imshow(grid, cmap=cmap, origin="upper", vmin=-2, vmax=2)

# Turn off axis labels and save the generated map image to a specified location
plt.axis('off')
plt.savefig("*where you want to put the map", bbox_inches='tight')
