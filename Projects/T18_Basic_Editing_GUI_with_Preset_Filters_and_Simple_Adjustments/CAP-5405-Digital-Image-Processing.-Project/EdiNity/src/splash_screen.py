import tkinter as tk
from PIL import Image, ImageTk
from home_screen2 import create_home_screen

def show_splash_screen(root):
    """
    Displays the splash screen when the application starts.
    
    Parameters:
    root (Tk): The main Tkinter root window.
    """
    # Create a frame for the splash screen with a dark background
    splash_frame = tk.Frame(root, bg="#2d2d2d")
    splash_frame.pack(fill=tk.BOTH, expand=True)

    # Load and display the splash image
    try:
        splash_image = Image.open("assets/edi N ity.png").resize((800, 650))
        splash_photo = ImageTk.PhotoImage(splash_image)
        splash_label = tk.Label(splash_frame, image=splash_photo)
        splash_label.image = splash_photo  # Keep a reference to avoid garbage collection
        splash_label.pack(fill=tk.BOTH, expand=True)
    except FileNotFoundError:
        # If the splash image is not found, display a placeholder label
        tk.Label(splash_frame, text="Splash Screen", font=("Arial", 24), bg="#2d2d2d", fg="white").pack(expand=True)

    # Automatically transition to the home screen after 2 seconds
    root.after(2000, lambda: transition_to_home(splash_frame, root))

def transition_to_home(splash_frame, root):
    """
    Transitions from the splash screen to the home screen.
    
    Parameters:
    splash_frame (Frame): The frame containing the splash screen content.
    root (Tk): The main Tkinter root window.
    """
    splash_frame.destroy()  # Remove the splash screen frame
    create_home_screen(root)  # Call the function to create the home screen
