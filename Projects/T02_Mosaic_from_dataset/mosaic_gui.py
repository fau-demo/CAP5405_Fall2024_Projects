import os
import json
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

# Constants
CACHE_FILE = "tile_cache.json"  # JSON file to store tile information

# Function to load tiles and cache their information
def load_tiles(dataset_path, tile_size):
    """
    Load tiles from the dataset and cache their histogram, average color, and usage info.
    Avoids recalculating if data exists in the cache.
    """
    # Load or initialize the cache
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            tile_cache = json.load(f)
    else:
        tile_cache = {}

    tiles = []
    for file_name in os.listdir(dataset_path):
        file_path = os.path.join(dataset_path, file_name)

        if file_path in tile_cache:
            # Use cached information
            tile_info = tile_cache[file_path]
        else:
            # Process new tile
            try:
                tile = Image.open(file_path).convert('RGB').resize(tile_size)
                avg_color = tuple(map(int, np.array(tile).mean(axis=(0, 1)).astype(int)))  # Convert to int
                histogram = list(map(int, tile.histogram()))  # Convert histogram to int
                tile_info = {
                    "path": file_path,
                    "avg_color": avg_color,
                    "histogram": histogram,
                    "used": False
                }
                tile_cache[file_path] = tile_info  # Save to cache
            except Exception as e:
                print(f"Error processing tile: {file_path}, {e}")
                continue

        # Add tile to list
        tiles.append({
            "image": Image.open(tile_info["path"]).convert('RGB').resize(tile_size),
            "avg_color": tile_info["avg_color"],
            "histogram": tile_info["histogram"],
            "used": tile_info["used"],
            "path": tile_info["path"]
        })

    # Save updated cache
    with open(CACHE_FILE, 'w') as f:
        json.dump(tile_cache, f)

    return tiles

# Function to reset the "used" status of all tiles
def reset_tile_usage():
    """Reset the 'used' status of all tiles in the cache."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            tile_cache = json.load(f)

        for tile_info in tile_cache.values():
            tile_info["used"] = False

        with open(CACHE_FILE, 'w') as f:
            json.dump(tile_cache, f)

# Function to match a tile to a block
def match_tile(block, tiles, mode="average", used_tiles=None):
    """
    Match a block with the best tile based on either average color or histogram comparison.
    """
    best_match = None
    best_score = float('inf')

    block_histogram = block.histogram() if mode == "histogram" else None
    block_avg_color = tuple(np.array(block).mean(axis=(0, 1)).astype(int)) if mode == "average" else None

    for tile in tiles:
        if tile["used"] and used_tiles is not None:
            continue  # Skip already used tiles

        # Compare based on selected mode
        if mode == "average":
            score = sum((bc - tc) ** 2 for bc, tc in zip(block_avg_color, tile["avg_color"]))
        elif mode == "histogram":
            score = sum(abs(bh - th) for bh, th in zip(block_histogram, tile["histogram"]))
        else:
            raise ValueError("Invalid match mode. Choose 'average' or 'histogram'.")

        if score < best_score:
            best_score = score
            best_match = tile

    if best_match:
        best_match["used"] = True  # Mark the tile as used
        if used_tiles is not None:
            used_tiles.add(best_match["path"])  # Track usage
    return best_match["image"]

# Function to create the mosaic
def create_mosaic(input_image_path, tiles, block_size, output_path, match_mode="average"):
    """
    Generate a mosaic for the input image using the provided tiles and save it.
    """
    input_image = Image.open(input_image_path).convert('RGB')
    input_width, input_height = input_image.size

    # Resize input image to fit evenly into blocks
    new_width = (input_width // block_size[0]) * block_size[0]
    new_height = (input_height // block_size[1]) * block_size[1]
    input_image = input_image.resize((new_width, new_height))

    mosaic = Image.new('RGB', (new_width, new_height))
    used_tiles = set()  # Track used tiles

    for y in range(0, new_height, block_size[1]):
        for x in range(0, new_width, block_size[0]):
            block = input_image.crop((x, y, x + block_size[0], y + block_size[1]))
            matching_tile = match_tile(block, tiles, mode=match_mode, used_tiles=used_tiles)
            mosaic.paste(matching_tile, (x, y))

    mosaic.save(output_path)
    return mosaic

# GUI Functions
def open_file():
    """Open a file dialog to select the input image."""
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
    if file_path:
        input_image_path.set(file_path)

def open_dataset():
    """Open a folder dialog to select the dataset folder."""
    folder_path = filedialog.askdirectory(title="Select Dataset Folder")
    if folder_path:
        dataset_path.set(folder_path)

def create_mosaic_button():
    """Handle the mosaic generation process."""
    input_image = input_image_path.get()
    dataset_folder = dataset_path.get()

    if not input_image or not dataset_folder:
        messagebox.showerror("Error", "Please select both an input image and a dataset folder.")
        return

    tile_size = int(tile_size_entry.get())
    output_path = "mosaic_output.jpg"

    # Load tiles
    print("Loading tiles...")
    tiles = load_tiles(dataset_folder, (tile_size, tile_size))
    print(f"Loaded {len(tiles)} tiles.")

    # Create mosaic
    print("Creating mosaic...")
    mosaic = create_mosaic(input_image, tiles, (tile_size, tile_size), output_path, match_mode=match_mode.get())
    print("Mosaic creation complete!")

    # Display the generated mosaic
    mosaic = mosaic.resize((500, 500))  # Resize for display
    mosaic_image = ImageTk.PhotoImage(mosaic)
    mosaic_label.config(image=mosaic_image)
    mosaic_label.image = mosaic_image  # Keep a reference to avoid garbage collection

# Initialize GUI
root = tk.Tk()
root.title("Mosaic Generator")
root.geometry("600x800")

# Input Image Path
input_image_path = tk.StringVar()
tk.Label(root, text="Select Input Image").pack()
tk.Button(root, text="Browse Image", command=open_file).pack()

# Dataset Path
dataset_path = tk.StringVar()
tk.Label(root, text="Select Dataset Folder").pack()
tk.Button(root, text="Browse Dataset", command=open_dataset).pack()

# Tile Size
tk.Label(root, text="Tile Size (px)").pack()
tile_size_entry = tk.Entry(root)
tile_size_entry.insert(0, "50")  # Default tile size
tile_size_entry.pack()

# Matching Mode
match_mode = tk.StringVar(value="average")
tk.Label(root, text="Matching Mode").pack()
tk.Radiobutton(root, text="Average Color", variable=match_mode, value="average").pack()
tk.Radiobutton(root, text="Histogram", variable=match_mode, value="histogram").pack()

# Generate Mosaic Button
tk.Button(root, text="Generate Mosaic", command=create_mosaic_button).pack()

# Mosaic Output Display
mosaic_label = tk.Label(root)
mosaic_label.pack()

# Reset Tile Usage Button
tk.Button(root, text="Reset Tile Usage", command=reset_tile_usage).pack()

# Run the GUI
root.mainloop()
