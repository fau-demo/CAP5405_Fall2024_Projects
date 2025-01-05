import cv2 # OpenCV library for image processing
import numpy as np # NumPy for array handling
from tkinter import * # Tkinter for GUI
from tkinter import filedialog # For file dialog to open/save images
from PIL import Image, ImageTk # PIL for image display in Tkinter

# Initialize variables
original_img = None # To store the original image
edited_img = None # To store the edited image
img_display = None  # For resizing of the image

# Load image using OpenCV and convert to RGB for display in Tkinter and display it on the canvas
def load_image():
    global original_img, edited_img, img_display
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")]) # Ask user to select a file
    if path:
        img = cv2.imread(path) # Read image using OpenCV
        if img is None:
            print("Error: Unable to load image. Please select a valid image file.")
            return
        original_img = img.copy() # Copy original image
        edited_img = img.copy() # Copy for edited image
        img_display = img.copy()  # Initialize the display image
        display_image(original_img, original_canvas) # Display original image
        display_image(edited_img, edited_canvas) # Display edited image
        enable_adjustments() # Enable adjustment

# Display image on Tkinter canvas
def display_image(img, target_canvas):
    if img is None:
        print("Error: No image to display")
        return
    try:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert image from BGR to RGB (Tkinter uses RGB)
        img_pil = Image.fromarray(img_rgb) # Convert NumPy array to PIL image
        img_tk = ImageTk.PhotoImage(img_pil) # Convert PIL image to Tkinter-compatible format
        
        # Set the image on the canvas and dynamically adjust canvas size
        target_canvas.config(width=img_pil.width, height=img_pil.height)
        target_canvas.create_image(0, 0, anchor=NW, image=img_tk) # Place the image on the canvas
        target_canvas.image = img_tk # Keep a reference to the image to prevent garbage collection
    except cv2.error as e:
        print(f"OpenCV error while converting image: {e}")

# Apply brightness and contrast adjustments
def apply_brightness_contrast():
    global edited_img
    if original_img is None:
        return
    brightness = brightness_slider.get() # Get the current brightness value
    contrast = contrast_slider.get() # Get the current contrast value
    edited_img = cv2.convertScaleAbs(original_img, alpha=contrast / 50, beta=brightness - 50) # Apply brightness and contrast
    # Resize edited image to match original image size
    edited_img = cv2.resize(edited_img, (original_img.shape[1], original_img.shape[0]))
    resize_image()  # Update the displayed image after resizing
    display_image(edited_img, edited_canvas) # Display the adjusted image

# Adjust color balance using sliders
def apply_curves():
    global edited_img
    if original_img is None:
        return
    r, g, b = red_slider.get(), green_slider.get(), blue_slider.get() # Get RGB values from sliders

    # Create lookup tables for each color channel (Red, Green, Blue)
    lut_red = np.clip(np.array([(i * r / 50) for i in range(256)], dtype=np.float32), 0, 255).astype(np.uint8)
    lut_green = np.clip(np.array([(i * g / 50) for i in range(256)], dtype=np.float32), 0, 255).astype(np.uint8)
    lut_blue = np.clip(np.array([(i * b / 50) for i in range(256)], dtype=np.float32), 0, 255).astype(np.uint8)

    # Apply lookup tables to the respective color channels
    r_img = cv2.LUT(original_img[:, :, 2], lut_red) # Red channel
    g_img = cv2.LUT(original_img[:, :, 1], lut_green) # Green channel
    b_img = cv2.LUT(original_img[:, :, 0], lut_blue) # Blue channel
    edited_img = cv2.merge((b_img, g_img, r_img)) # Merge channels back together
    # Resize edited image to match original image size
    edited_img = cv2.resize(edited_img, (original_img.shape[1], original_img.shape[0]))
    resize_image()  # Ensure edited image is resized correctly
    display_image(edited_img, edited_canvas) # Display adjusted image

# Reset adjustments to the original
def reset_image():
    global edited_img
    if original_img is None:
        return
    edited_img = original_img.copy() # Reset to original image
    display_image(edited_img, edited_canvas) # Display the reset image
    brightness_slider.set(50) # Reset sliders to default values
    contrast_slider.set(50)
    red_slider.set(50)
    green_slider.set(50)
    blue_slider.set(50)

# Save the edited image to a file
def save_image():
    if edited_img is None:
        print("Error: No image to save.")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]) # Ask user for save location
    if save_path: # If a location is selected
        cv2.imwrite(save_path, edited_img) # Save the image
        print(f"Image saved to: {save_path}")

# Enable UI elements (sliders and buttons) after an image is loaded
def enable_adjustments():
    brightness_slider.config(state=NORMAL)
    contrast_slider.config(state=NORMAL)
    red_slider.config(state=NORMAL)
    green_slider.config(state=NORMAL)
    blue_slider.config(state=NORMAL)
    reset_button.config(state=NORMAL)
    save_button.config(state=NORMAL)

# Resize both original and edited images based on slider value
def resize_image():
    global original_img, edited_img
    if original_img is None: # If no image is loaded
        return

    scale_percentage = resize_slider.get() # Get the resize percentage from the slider

    # Resize the original image
    width_original = int(original_img.shape[1] * scale_percentage / 100)
    height_original = int(original_img.shape[0] * scale_percentage / 100)
    resized_original_img = cv2.resize(original_img, (width_original, height_original), interpolation=cv2.INTER_AREA)
    display_image(resized_original_img, original_canvas) # Display resized original image

    # Resize edited image 
    width_edited = int(edited_img.shape[1] * scale_percentage / 100)
    height_edited = int(edited_img.shape[0] * scale_percentage / 100)
    resized_edited_img = cv2.resize(edited_img, (width_edited, height_edited), interpolation=cv2.INTER_AREA)
    display_image(resized_edited_img, edited_canvas) # Display resized edited image

# GUI setup
root = Tk() # Create the main window
root.title("Image Editing Tool - Adjustments") # Set window title

# Frames for layout
control_frame = Frame(root) # Frame for controls (sliders, buttons)
control_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

canvas_frame = Frame(root) # Frame for displaying images
canvas_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# Create Original and edited image canvases
original_canvas = Canvas(canvas_frame, bg="gray") # Canvas for original image
original_canvas.grid(row=0, column=0, padx=5, pady=5)
original_canvas.create_text(250, 200, text="Original Image", fill="white") # Text label for original image

# Move the edited image canvas to the right side of the original image canvas
edited_canvas = Canvas(canvas_frame, bg="gray")
edited_canvas.grid(row=0, column=1, padx=5, pady=5)  # Position edited image canvas to the right
edited_canvas.create_text(250, 200, text="Edited Image", fill="white") # Text label for edited image

# Controls buttons & Sliders for adjustments
load_button = Button(control_frame, text="Load Image", command=load_image) # Button to load an image
load_button.grid(row=0, column=0, padx=5, pady=5)

# Sliders for adjusting brightness, contrast, and color balance
brightness_slider = Scale(control_frame, from_=0, to=100, label="Brightness", orient=HORIZONTAL, command=lambda _: apply_brightness_contrast())
brightness_slider.set(50)
brightness_slider.grid(row=1, column=0, padx=5, pady=5)

contrast_slider = Scale(control_frame, from_=0, to=100, label="Contrast", orient=HORIZONTAL, command=lambda _: apply_brightness_contrast())
contrast_slider.set(50)
contrast_slider.grid(row=2, column=0, padx=5, pady=5)

red_slider = Scale(control_frame, from_=0, to=100, label="Red", orient=HORIZONTAL, command=lambda _: apply_curves())
red_slider.set(50)
red_slider.grid(row=3, column=0, padx=5, pady=5)

green_slider = Scale(control_frame, from_=0, to=100, label="Green", orient=HORIZONTAL, command=lambda _: apply_curves())
green_slider.set(50)
green_slider.grid(row=4, column=0, padx=5, pady=5)

blue_slider = Scale(control_frame, from_=0, to=100, label="Blue", orient=HORIZONTAL, command=lambda _: apply_curves())
blue_slider.set(50)
blue_slider.grid(row=5, column=0, padx=5, pady=5)

resize_slider = Scale(control_frame, from_=10, to=200, label="Resize Image (%)", orient=HORIZONTAL, command=lambda _: resize_image())
resize_slider.set(100)
resize_slider.grid(row=6, column=0, padx=5, pady=5)

# Buttons for resetting and saving images
reset_button = Button(control_frame, text="Reset", command=reset_image)
reset_button.grid(row=7, column=0, padx=5, pady=5)

save_button = Button(control_frame, text="Save", command=save_image)
save_button.grid(row=8, column=0, padx=5, pady=5)

root.mainloop() # Run the Tkinter main loop