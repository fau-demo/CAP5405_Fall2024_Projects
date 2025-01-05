import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from shared import add_logo, create_menu
from utilities import upload_function, open_gallery_folder

def set_background(canvas, bg_image_path):
    """
    Set a background image on the given canvas.

    Parameters:
    canvas (Canvas): The canvas where the background image will be applied.
    bg_image_path (str): Path to the background image file.
    """
    try:
        # Open and resize the background image to fit the window size
        bg_image = Image.open(bg_image_path).resize((1400, 750), Image.ANTIALIAS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        canvas.bg_image = bg_photo  # Keep a reference to prevent garbage collection
        canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)  # Place the background image
    except FileNotFoundError:
        # Print an error message if the background image is not found
        print(f"Background image not found: {bg_image_path}")

def create_home_screen(root):
    """
    Create the home screen with a background image, logo, and interactive buttons.

    Parameters:
    root (Tk): The main Tkinter root window.
    """
    # Clear all existing widgets on the root window
    for widget in root.winfo_children():
        widget.destroy()

    # Paths for the background image and logo
    bg_image_path = "assets/Create. Enhance. Inspire..png"
    logo_path = "assets/logo_head.png"

    # Create a canvas to hold the background and widgets
    canvas = tk.Canvas(root, width=1400, height=750, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Set the background image on the canvas
    set_background(canvas, bg_image_path)

    # Add the logo using the shared utility function
    add_logo(canvas, logo_path, x=10, y=10)

    try:
        # Load and resize the "Upload" button image
        upload_icon = Image.open("assets/upload.png").resize((100, 100), Image.ANTIALIAS)
        upload_photo = ImageTk.PhotoImage(upload_icon)

        # Create the "Upload" button
        upload_button = tk.Button(
            root,
            image=upload_photo,
            bg="#eeece7",
            activebackground="#eeece7",
            borderwidth=0,
            command=lambda: upload_function(root)  # Calls the upload function
        )
        upload_button.image = upload_photo  # Keep a reference to prevent garbage collection
        upload_button.place(x=333, y=500, anchor="center")  # Position the button on the left half

    except FileNotFoundError:
        # Print an error message if the upload button image is not found
        print("Upload button image not found: assets/upload.png")

    try:
        # Load and resize the "Gallery" button image
        gallery_icon = Image.open("assets/image.png").resize((100, 100), Image.ANTIALIAS)
        gallery_photo = ImageTk.PhotoImage(gallery_icon)

        # Create the "Gallery" button
        gallery_button = tk.Button(
            root,
            image=gallery_photo,
            bg="#2d3030",
            activebackground="#2d3030",
            borderwidth=0,
            command=lambda: open_gallery_folder(root)  # Calls the gallery function
        )
        gallery_button.image = gallery_photo  # Keep a reference to prevent garbage collection
        gallery_button.place(x=1050, y=500, anchor="center")  # Position the button on the right half

    except FileNotFoundError:
        # Print an error message if the gallery button image is not found
        print("Gallery button image not found: assets/image.png")

    # Create a canvas for the hamburger menu button
    menu_canvas = tk.Canvas(canvas, width=30, height=30, bg="#2d3030", bd=0, highlightthickness=0)

    # Draw the three horizontal lines for the hamburger icon
    menu_canvas.create_line(5, 7, 30, 7, fill="#eeece7", width=3)  # Top line
    menu_canvas.create_line(5, 15, 30, 15, fill="#eeece7", width=3)  # Middle line
    menu_canvas.create_line(5, 23, 30, 23, fill="#eeece7", width=3)  # Bottom line

    # Place the menu canvas in the top-right corner
    canvas.create_window(
        1340, 10,  # X and Y position for the top-right corner
        anchor=tk.NE,
        window=menu_canvas
    )

    # Bind the menu canvas to open the hamburger menu when clicked
    menu_canvas.bind(
        "<Button-1>",
        lambda e: create_menu(root, x=menu_canvas.winfo_rootx(), y=menu_canvas.winfo_rooty() + 40)
    )
