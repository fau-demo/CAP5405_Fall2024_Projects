import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image
from weighted_voronoi_stippling import voronoi_stipple

# Initialize the GUI application
app = ctk.CTk()
app.title("Voronoi Stippling GUI")
app.geometry("600x600")

# Variables to store user inputs
img_path = tk.StringVar()
stipple_points = tk.IntVar(value=8000)
lloyd_iters = tk.IntVar(value=30)
qlevels = tk.IntVar(value=0)
seed = tk.IntVar(value=111)
random_sampling = tk.BooleanVar(value=True)
plot = tk.BooleanVar(value=True)
save = tk.BooleanVar(value=False)
quantization_enabled = tk.BooleanVar(value=False)
custom_seed_enabled = tk.BooleanVar(value=False)
image_preview = None

# Open file dialog and set image path
def select_file():
    global image_preview
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff")])
    if file_path:
        img_path.set(file_path)
        load_image(file_path)

# Load and display the selected image using CTkImage
def load_image(file_path):
    global image_preview
    try:
        img = Image.open(file_path)
        img.thumbnail((300, 300))
        image_preview = ctk.CTkImage(light_image=img, size=(300, 300))
        image_label.configure(image=image_preview, text="")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load image: {e}")

# Validate and clamp entry input
def validate_and_clamp(value, min_value, max_value, variable):
    try:
        value = int(value)
        value = max(min(value, max_value), min_value)
    except ValueError:
        value = variable.get()
    variable.set(value)

# Toggle quantization slider
def toggle_quantization():
    if quantization_enabled.get():
        qlevels_slider.configure(state="normal")
        qlevels_entry.configure(state="normal")
    else:
        qlevels_slider.configure(state="disabled")
        qlevels_entry.configure(state="disabled")
        qlevels.set(0)

# Toggle seed input
def toggle_seed():
    if custom_seed_enabled.get():
        seed_entry.configure(state="normal")
    else:
        seed_entry.configure(state="disabled")
        seed.set(111)

# Generate Voronoi stipple
def generate_voronoi():
    try:
        if not img_path.get():
            messagebox.showerror("Error", "Please select an image file.")
            return

        voronoi_stipple(
            img_path=img_path.get(),
            stipple_points=stipple_points.get(),
            gray_levels=qlevels.get(),
            lloyd_iters=lloyd_iters.get(),
            random_sampling=random_sampling.get(),
            plot=plot.get(),
            save=save.get()
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Layout Frames
left_frame = ctk.CTkFrame(app, width=200)  # Make left frame 25% thinner
left_frame.pack(side="left", fill="y", padx=10, pady=10)

right_frame = ctk.CTkFrame(app)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Left Frame Widgets (Inputs)
ctk.CTkLabel(left_frame, text="Stipple Points (100 - 50000):").pack(pady=5, anchor="w")
stipple_points_slider = ctk.CTkSlider(left_frame, from_=100, to=50000, variable=stipple_points)
stipple_points_slider.pack(pady=5, anchor="w")
stipple_points_entry = ctk.CTkEntry(left_frame, textvariable=stipple_points)
stipple_points_entry.pack(pady=5, anchor="w")
stipple_points_entry.bind("<FocusOut>", lambda e: validate_and_clamp(stipple_points_entry.get(), 100, 50000, stipple_points))

ctk.CTkLabel(left_frame, text="Lloyd Iterations (0 - 100):").pack(pady=5, anchor="w")
lloyd_iters_slider = ctk.CTkSlider(left_frame, from_=0, to=100, variable=lloyd_iters)
lloyd_iters_slider.pack(pady=5, anchor="w")
lloyd_iters_entry = ctk.CTkEntry(left_frame, textvariable=lloyd_iters)
lloyd_iters_entry.pack(pady=5, anchor="w")
lloyd_iters_entry.bind("<FocusOut>", lambda e: validate_and_clamp(lloyd_iters_entry.get(), 0, 100, lloyd_iters))

quantization_checkbox = ctk.CTkCheckBox(left_frame, text="Quantization (0 - 128)", variable=quantization_enabled, command=toggle_quantization)
quantization_checkbox.pack(pady=5, anchor="w")
qlevels_slider = ctk.CTkSlider(left_frame, from_=0, to=128, variable=qlevels, state="disabled")
qlevels_slider.pack(pady=5, anchor="w")
qlevels_entry = ctk.CTkEntry(left_frame, textvariable=qlevels, state="disabled")
qlevels_entry.pack(pady=5, anchor="w")
qlevels_entry.bind("<FocusOut>", lambda e: validate_and_clamp(qlevels_entry.get(), 0, 128, qlevels))

custom_seed_checkbox = ctk.CTkCheckBox(left_frame, text="Custom Seed", variable=custom_seed_enabled, command=toggle_seed)
custom_seed_checkbox.pack(pady=5, anchor="w")
seed_entry = ctk.CTkEntry(left_frame, textvariable=seed, state="disabled")
seed_entry.pack(pady=5, anchor="w")

random_sampling_checkbox = ctk.CTkCheckBox(left_frame, text="Random Sampling", variable=random_sampling)
random_sampling_checkbox.pack(pady=5, anchor="w")

plot_checkbox = ctk.CTkCheckBox(left_frame, text="Plot", variable=plot)
plot_checkbox.pack(pady=5, anchor="w")

save_checkbox = ctk.CTkCheckBox(left_frame, text="Save", variable=save)
save_checkbox.pack(pady=5, anchor="w")

generate_button = ctk.CTkButton(left_frame, text="Generate Weighted Voronoi Stipple", command=generate_voronoi)
generate_button.pack(pady=20, anchor="w")

# Right Frame Widgets (File Selection and Image Display)
ctk.CTkLabel(right_frame, text="Select Image:").pack(pady=10)
ctk.CTkButton(right_frame, text="Browse", command=select_file).pack(pady=10)
image_label = ctk.CTkLabel(right_frame, text="")
image_label.pack(pady=10)

# Start the GUI application
app.mainloop()
