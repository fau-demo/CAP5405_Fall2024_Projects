# Importing required libraries
import ttkbootstrap as ttk  # Enhanced styling and layout library for Tkinter applications
from ttkbootstrap.constants import *  # Constants for ttkbootstrap themes and styling
from tkinter import filedialog  # Standard library for file dialog (load/save)
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageOps, ImageDraw  # Powerful library for image processing
import math  # Math library for calculations
from styles import apply_styles, create_load_button, create_save_button  # Custom styles and button creation functions
from filters import *  # Import all custom filter implementations


# Global variables for managing state
img = None  # Original image loaded by the user
processed_img = None  # Processed version of the image
filter_states = {}  # Tracking filter states and their intensities
previews = {}  # Storing preview thumbnails for predefined filters
history = []  # Stacking to store image states for undo functionality
original_label = None  # Labeling for the original image
filtered_label = None  # Labeling for the filtered image
slider = None  # Intensity adjustment slider
filter_dropdown=None 


# Filter mapping to connect dropdown choices with respective functions
filter_functions = {
     "Grayscale": apply_grayscale,  # Applying grayscale filter
    "Sepia": apply_sepia,  # Applying sepia filter
    "Blur": apply_blur,  # Applying blur filter
    "Sharpen": apply_sharpen,  # Applying sharpen filter
    "Brightness Adjustment": adjust_brightness,  # Adjusting brightness
    "Contrast Adjustment": adjust_contrast,  # Adjusting contrast
    "Saturation Adjustment": adjust_saturation,  # Adjusting saturation
    "Vignette": apply_vignette,  # Applying vignette effect
    "Edge Detection": apply_edgeDetection,  # Applying edge detection filter
    "Emboss": apply_emboss,  # Applying emboss effect
    "Artistic Filter": apply_artistic_filter,  # Applying artistic filter
}

# Predefined filters with specific effects
predefined_filters = [
    ("Polaroid Effect", apply_polaroid_effect),  # Apply Polaroid effect
    ("Invert Colors", apply_invert_colors),  # Invert image colors
    ("Oil Painting", apply_oil_painting_effect),  # Apply oil painting effect
    ("Watercolor", apply_watercolor_effect),  # Apply watercolor effect
]

def update_canvases():
    """
    Updating both canvases with the original and processed images.
    Ensures images are resized and centered within their respective canvases.
    """
    if img:  # Checking if an image is loaded
        # Original image displayed on the left canvas
        canvas_width, canvas_height = 900, 650  # Seting fixed canvas dimensions
        img_width, img_height = img.size  # Getting dimensions of the original image
        ratio = min(canvas_width / img_width, canvas_height / img_height)  # Calculating scaling ratio
        new_width, new_height = int(img_width * ratio), int(img_height * ratio)  # Resizing dimensions
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Resizing using high-quality resampling
        img_tk = ImageTk.PhotoImage(img_resized)  # Converting resized image to Tkinter-compatible format
        original_canvas.itemconfig(original_image_on_canvas, image=img_tk)  # Updating image on the canvas
        original_canvas.image = img_tk  # Preventing garbage collection of the image object
        # Centering the image on the canvas
        original_canvas.coords(original_image_on_canvas, canvas_width // 2, canvas_height // 2)

    if processed_img:  # Checking if a processed image exists
        # Processed image displayed on the right canvas
        canvas_width, canvas_height = 900, 650  # Seting fixed canvas dimensions
        img_width, img_height = processed_img.size  # Geting dimensions of the processed image
        ratio = min(canvas_width / img_width, canvas_height / img_height)  # Calculating scaling ratio
        new_width, new_height = int(img_width * ratio), int(img_height * ratio)  # Resizing dimensions
        img_resized = processed_img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Resizing processed image
        img_tk = ImageTk.PhotoImage(img_resized)  # Converting resized image to Tkinter-compatible format
        processed_canvas.itemconfig(processed_image_on_canvas, image=img_tk)  # Updating image on the canvas
        processed_canvas.image = img_tk  # Preventing garbage collection of the image object
        processed_canvas.coords(processed_image_on_canvas, canvas_width // 2, canvas_height // 2) # Centering the processed image on the canvas

def apply_predefined_filter(filter_func):
    """
    Applying a predefined filter to the image.
    Updates the processed image and maintains a history for undo functionality.
    """
    global processed_img, history
    if not img:
        return

    # Saving the current state before applying the filter
    if processed_img:
        history.append(processed_img.copy())

    # Applying the filter without modifying image size
    processed_img = filter_func(img.copy())
    update_canvases()  # Display changes on the canvases



# Helper Functions
def update_canvas():
    """
    Updating the canvas with the processed image while maintaining its aspect ratio.
    Dynamically resizes the image based on canvas dimensions.
    """
    if processed_img:
        # Getting canvas dimensions
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        # Getting the original image dimensions
        img_width, img_height = processed_img.size

        # Calculating the new dimensions while maintaining the aspect ratio
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        # Resizing the image
        img_resized = processed_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Converting to Tkinter-compatible image
        img_tk = ImageTk.PhotoImage(img_resized)

        # Centering the image on the canvas
        canvas.itemconfig(image_on_canvas, image=img_tk)
        canvas.coords(image_on_canvas, canvas_width // 2, canvas_height // 2)
        canvas.image = img_tk  # Prevent garbage collection

        canvas.image = img_tk  # Prevent garbage collection
        update_canvases()

def on_filter_change(*args):
    """
    Applying the selected filter from the dropdown menu and adjust its intensity.
    Saves the current image state to history for undo functionality.
    """
    global processed_img
    if not img:
        return

    # Getting selected filter and slider intensity
    filter_type = filter_var.get()
    intensity = slider.get() / 10  # Normalizing intensity to 0-2 range

    # Saving the current state before applying a new filter
    if processed_img:
        history.append(processed_img.copy())
    filter_states[filter_type] = intensity
    base_image = img.copy()

    # Applying each filter with its stored intensity
    for f_type, f_intensity in filter_states.items():
        if f_type in filter_functions:
            base_image = filter_functions[f_type](base_image, f_intensity)

    processed_img = base_image  # Updating processed image

    update_canvases()  # Refreshing the display



def on_slider_change(*args):
    """
     Updating the image when the intensity slider is adjusted.
    Reapplies the currently selected filter with the new intensity.
    """
    on_filter_change()  # Indentation fixed here


# Inside load_image function, align predefined filters directly below the image
def load_image():
    """Loading an image and display predefined filters below it."""
    global img, processed_img, filter_states, previews,filter_dropdown,filtered_label,original_label
    try:
        # Opening file dialog to select an image
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            # Loading and process the image
            img_original = Image.open(file_path).convert("RGB")
            img = img_original.copy()  # Work with a copy of the original
            processed_img = img_original.copy()
            filter_states = {} # Reset applied filters
            generate_filter_previews()
            update_canvases()

            # Enabling the intensity slider
            if filter_dropdown:
                filter_dropdown.config(state="readonly")
            if slider:
                slider.config(state="normal")
            

              # Dynamically creating and displaying the labels
            if original_label is None:
                original_label = ttk.Label(
                    comparison_frame, text="Original Image",
                    font=("Helvetica", 14, "bold"), anchor=CENTER
                )
                original_label.grid(row=1, column=0, pady=(10, 0))

            if filtered_label is None:
                filtered_label = ttk.Label(
                    comparison_frame, text="Filtered Image",
                    font=("Helvetica", 14, "bold"), anchor=CENTER
                )
                filtered_label.grid(row=1, column=1, pady=(10, 0))

            # Clearing existing filter buttons
            for child in filters_frame.winfo_children():
                child.destroy()

            # Populating filters dynamically
            for filter_name, filter_func in predefined_filters:
                # Framing for each filter button and preview
                filter_button_frame = ttk.Frame(filters_frame)
                filter_button_frame.pack(side=LEFT, padx=10, pady=5)

                # Filtering preview image
                if filter_name in previews:
                    filter_preview = ttk.Label(filter_button_frame, image=previews[filter_name])
                    filter_preview.pack(anchor=CENTER)

                # Filter button
                ttk.Button(
                    filter_button_frame,
                    text=filter_name,
                    command=lambda f=filter_func: apply_predefined_filter(f),
                    bootstyle="secondary"
                ).pack(anchor=CENTER)

            # Ensuring filters_frame appears below the canvas
            filters_frame.pack(anchor=CENTER, pady=10)
    except Exception as e:
        print(f"Error loading image: {e}")



def save_image():
    """
    Opening a file dialog to save the currently processed image.
    Allows the user to save the image in JPG or PNG format.
    """
    if processed_img:
        # Opening file dialog to specify save location and format
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
        )
        if file_path:
            processed_img.save(file_path)  # Saving the processed image to the specified file path


def reset_filters():
    """Reseting all filters and restore the original image."""
    global processed_img, filter_states
    if img:
        processed_img = img.copy()  # Restoring the original image
        filter_states = {}  # Clearing all filter states
        slider.set(0)  # Reseting the slider to 0
        filter_var.set("Grayscale")  # Reseting the filter selection to "Grayscale"
        update_canvases()  # Updating the canvas with the original image

def undo_last_action():
    """Undo the last applied filter."""
    global processed_img, filter_states
    if history:
        processed_img = history.pop()  # Restoring the last state
        # Reset filter_states to match the restored image
        if filter_states:
            last_filter = list(filter_states.keys())[-1]
            last_intensity = filter_states[last_filter]
            slider.set(int(last_intensity * 10))  # Updating slider position (0-20 scale)
            filter_states.pop(last_filter)  # Removing the last filter from the states
            update_canvases() 
        else:
            slider.set(0)  # Reset the slider to the default if no filters are active
        update_canvases()  # Update the canvas with the restored image



def generate_filter_previews():
    """Generating small previews for each filter."""
    global previews
    if not img:
        return

    # Resizing original image for thumbnails
    thumbnail = img.resize((100, 100), Image.Resampling.LANCZOS)

    # Generating previews for each filter
    previews = {}
    for filter_name, filter_func in predefined_filters:
        try:
            filtered_preview = filter_func(thumbnail.copy())
            previews[filter_name] = ImageTk.PhotoImage(filtered_preview)
        except Exception as e:
            print(f"Error generating preview for {filter_name}: {e}")



# Main App
root = ttk.Window(themename="solar")  # Creating the root window using the 'solar' theme
root.title("Image Filters Tool")
root.state('zoomed') 
root.geometry("1000x1000")

# UI Elements for the top section (load and save buttons)
filter_var = ttk.StringVar(value="Grayscale")  # Default filter selection
ttk.Label(root, text="Image Filters Tool", font=("Helvetica", 24, "bold"), anchor=CENTER).pack(pady=20)
frame_top = ttk.Frame(root)
frame_top.pack(fill=X)
load_button = create_load_button(frame_top, load_image, root.style)  # Pass load_image as a callback
load_button.pack(side="left", padx=20)
save_button = create_save_button(frame_top, save_image, root.style)
save_button.pack(side="right", padx=20)

# Container for the image and filters
image_container_frame = ttk.Frame(root)
image_container_frame.pack(fill=X, expand=True, pady=10)

# Frame to hold two canvases for side-by-side comparison
comparison_frame = ttk.Frame(root)
comparison_frame.pack(fill=BOTH, expand=True, pady=10)

# Using grid layout for the comparison frame
comparison_frame.columnconfigure(0, weight=1)  # First column (original canvas)
comparison_frame.columnconfigure(1, weight=1)  # Second column (processed canvas)
comparison_frame.rowconfigure(0, weight=1)  # Allowing canvases to expand vertically

# Canvas for the original image
original_canvas = ttk.Canvas(comparison_frame, width=600, height=480)
original_canvas.grid(row=0, column=0, padx=(150, 0), pady=0, sticky="nsew")  # Using grid instead of pack
original_image_on_canvas = original_canvas.create_image(300, 250, anchor=CENTER)

# Canvas for the processed image
processed_canvas = ttk.Canvas(comparison_frame, width=600, height=480)
processed_canvas.grid(row=0, column=1, padx=(0,350), pady=0, sticky="nsew")  # Using grid instead of pack
processed_image_on_canvas = processed_canvas.create_image(300, 250, anchor=CENTER)


# Predefined Filters Section
filters_frame = ttk.Frame(image_container_frame)
filters_frame.pack(anchor=CENTER, pady=0)  # Positioned directly below the canvas
filters_frame.pack_forget()

# Inside load_image, populate the filters_frame dynamically
for filter_name, filter_func in predefined_filters:
    filter_button_frame = ttk.Frame(filters_frame)
    filter_button_frame.pack(side=LEFT, padx=10, pady=5)  # Aligning filters horizontally
    if filter_name in previews:
        filter_preview = ttk.Label(filter_button_frame, image=previews[filter_name])
        filter_preview.pack()
    ttk.Button(
        filter_button_frame,
        text=filter_name,
        command=lambda f=filter_func: apply_predefined_filter(f),
        bootstyle="secondary",
        cursor="hand2"
    ).pack(pady=5)


# Controling frame for selecting filters and adjusting intensity
# Adjusting controls frame
control_frame = ttk.Frame(root)
control_frame.pack(side=BOTTOM, pady=10)  # Ensuring it's always at the bottom

ttk.Label(control_frame, text="Choose Filter:", style="TLabel").grid(row=0, column=0, sticky=W, padx=5)
filter_dropdown=filter_dropdown=ttk.Combobox(
    control_frame, 
    textvariable=filter_var, 
    values=list(filter_functions.keys()), 
    bootstyle="info", 
    state="disabled",
    cursor="hand2"
)
filter_dropdown.grid(row=0, column=1, padx=10, sticky=W)
filter_var.trace_add("write", on_filter_change)  # Applying filter when the selection changes

# Slider for adjusting filter intensity
ttk.Label(control_frame, text="Adjust Intensity/Radius:", style="TLabel").grid(row=1, column=0, sticky=W, padx=5)
slider = ttk.Scale(control_frame, from_=0, to=20, command=on_slider_change, bootstyle="success", state="disabled",cursor="hand2")
slider.grid(row=1, column=1, padx=10, pady=10)

# Reset and undo button to clear filters and revert to the original image
ttk.Button(control_frame, text="Reset", command=reset_filters, bootstyle="warning", cursor="hand2").grid(row=1, column=2, padx=10, sticky=E)
ttk.Button(control_frame, text="Undo", command=undo_last_action, bootstyle="warning", cursor="hand2").grid(row=1, column=3, padx=10, sticky=E)


# Footer section
footer = ttk.Frame(root)
footer.pack(side="bottom", fill="x", pady=0) 
ttk.Label(footer, text="Image Filters Tool © 2024", anchor=CENTER, font=("Helvetica", 10), foreground="white").pack()
root.pack_propagate(False)

# Start the Tkinter main event loop
root.mainloop()