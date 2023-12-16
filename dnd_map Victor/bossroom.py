# Import necessary libraries
import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# Function to generate a DnD boss room layout
def generate_dnd_boss_room_layout_v8(grid_size):
    # Define room types and their maximum counts
    room_types = {
        "Throne Room": 1, "Entrance": 1, "Bathroom": 1, "Sleeping Area": 1,
        "Torture Room": 1, "Guard Room": 3, "Treasure Room": 2, "Kitchen": 1
    }
    room_counts = {room: 0 for room in room_types}

    # Initialize the grid
    grid = [["" for _ in range(grid_size)] for _ in range(grid_size)]

    # Place the Throne Room farthest from the Entrance
    throne_room_pos = (grid_size - 1, grid_size - 1)
    grid[throne_room_pos[0]][throne_room_pos[1]] = "Throne Room"
    room_counts["Throne Room"] += 1

    # Place the Entrance at least 3 spaces away from the Throne Room
    possible_entrance_positions = [(i, j) for i in range(grid_size) for j in range(grid_size) 
                                   if abs(i - throne_room_pos[0]) + abs(j - throne_room_pos[1]) >= 3]
    entrance_pos = random.choice(possible_entrance_positions)
    grid[entrance_pos[0]][entrance_pos[1]] = "Entrance"
    room_counts["Entrance"] += 1

    # Place the Sleeping Area next to the Throne Room
    sleeping_area_choices = [(throne_room_pos[0] - 1, throne_room_pos[1]), 
                             (throne_room_pos[0], throne_room_pos[1] - 1)]
    sleeping_area_pos = random.choice(sleeping_area_choices)
    grid[sleeping_area_pos[0]][sleeping_area_pos[1]] = "Sleeping Area"
    room_counts["Sleeping Area"] += 1

    # Place the Bathroom next to the Sleeping Area
    bathroom_choices = [(sleeping_area_pos[0] + dr, sleeping_area_pos[1] + dc) 
                        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                        if 0 <= sleeping_area_pos[0] + dr < grid_size and 0 <= sleeping_area_pos[1] + dc < grid_size]
    bathroom_pos = random.choice(bathroom_choices)
    grid[bathroom_pos[0]][bathroom_pos[1]] = "Bathroom"
    room_counts["Bathroom"] += 1
     
    edge_positions = [(i, j) for i in range(grid_size) for j in range(grid_size) 
                      if i == 0 or i == grid_size - 1 or j == 0 or j == grid_size - 1]
    entrance_pos = random.choice(edge_positions)
    grid[entrance_pos[0]][entrance_pos[1]] = "Entrance"
    room_counts["Entrance"] += 1

    # Function to check if placement of a room is valid
    def is_valid_placement(r, c, room):
        if room_counts[room] >= room_types[room]:
            return False

        if room == "Guard Room":
            near_entrance_or_throne = any(grid[nr][nc] in ["Entrance", "Throne Room"] for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                                          for nr, nc in [(r + dr, c + dc)] if 0 <= nr < grid_size and 0 <= nc < grid_size)
            return near_entrance_or_throne

        if room == "Kitchen":
            near_sleeping = any(grid[nr][nc] == "Sleeping Area" for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                                for nr, nc in [(r + dr, c + dc)] if 0 <= nr < grid_size and 0 <= nc < grid_size)
            not_near_entrance = not any(grid[nr][nc] == "Entrance" for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                                        for nr, nc in [(r + dr, c + dc)] if 0 <= nr < grid_size and 0 <= nc < grid_size)
            return near_sleeping and not_near_entrance

        return True

    # Assign rooms to the grid, ensuring all spaces are filled
    for r in range(grid_size):
        for c in range(grid_size):
            if grid[r][c] == "":
                valid_rooms = [room for room in room_types if is_valid_placement(r, c, room)]
                if not valid_rooms:
                    chosen_room = "Guard Room"  # Default room if no valid room is available
                else:
                    chosen_room = random.choice(valid_rooms)
                grid[r][c] = chosen_room
                room_counts[chosen_room] += 1

    return grid

# Function to check if placement of a room is valid (part of the previous function)

# Function to plot the DnD boss room layout
def plot_dnd_room_layout(layout):
    # Mapping room types to colors
    room_colors = {
        "Throne Room": "gold",
        "Entrance": "grey",
        "Bathroom": "lightblue",
        "Sleeping Area": "pink",
        "Torture Room": "darkred",
        "Guard Room": "green",
        "Treasure Room": "purple",
        "Kitchen": "orange",
        "": "white"  # Color for empty rooms
    }

    # Create a numeric grid for coloring
    color_grid = np.zeros((len(layout), len(layout[0])), dtype=int)
    for i, row in enumerate(layout):
        for j, room in enumerate(row):
            color_grid[i, j] = list(room_colors.keys()).index(room)

    # Create a colormap
    cmap = mcolors.ListedColormap(room_colors.values())

    # Plot the grid
    fig, ax = plt.subplots()
    ax.matshow(color_grid, cmap=cmap)

    # Label the rooms
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            text = layout[i][j] if layout[i][j] else "Empty"
            ax.text(j, i, text, ha='center', va='center', fontsize=8)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('DnD Boss Room Layout')

    plt.show()

# Generate and plot the DnD boss room layout
dnd_room_layout = generate_dnd_boss_room_layout_v8(4)
plot_dnd_room_layout(dnd_room_layout)
