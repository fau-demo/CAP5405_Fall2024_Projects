from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Toplevel, Label, messagebox

def on_hover(event, label):
    """Change the background color of the label when the mouse hovers over it."""
    label.config(bg="#3A3A3A")

def on_leave(event, label):
    """Reset the background color of the label when the mouse leaves."""
    label.config(bg="#2D3030")

def close_menu(menu_popup):
    """Destroy the popup menu when the user clicks outside it or chooses an option."""
    menu_popup.destroy()

def create_menu(root, x, y):
    """
    Create a custom popup menu at the specified screen position (x, y).
    
    Parameters:
    root (Tk): The root window where the popup is created.
    x (int): X-coordinate for the popup position.
    y (int): Y-coordinate for the popup position.
    """
    menu_popup = Toplevel(root)
    menu_popup.overrideredirect(True)  # Remove window decorations (title bar, etc.)
    menu_popup.attributes('-alpha', 0.8)  # Make the popup semi-transparent
    menu_popup.config(bg="#2D3030")  # Set a dark grey background

    # Set dimensions and adjust position to prevent overflow off the screen
    popup_width = 200
    popup_height = 180
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = min(x, screen_width - popup_width - 10)
    y = min(y, screen_height - popup_height - 10)
    menu_popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    # Configure menu style
    menu_font = ("Arial", 12, "bold")
    normal_bg = "#2D3030"
    text_color = "#eeece7"

    # "Open Recent Files" Option
    recent_files = Label(
        menu_popup,
        text="Open Recent Files",
        font=menu_font,
        bg=normal_bg,
        fg=text_color,
        anchor="w",
        padx=10
    )
    recent_files.pack(fill="x", pady=5)
    recent_files.bind("<Enter>", lambda e: on_hover(e, recent_files))
    recent_files.bind("<Leave>", lambda e: on_leave(e, recent_files))
    recent_files.bind("<Button-1>", lambda e: messagebox.showinfo("Recent Files", "Show recent files functionality"))

    # "Exit Application" Option
    exit_app = Label(
        menu_popup,
        text="Exit Application",
        font=menu_font,
        bg=normal_bg,
        fg=text_color,
        anchor="w",
        padx=10
    )
    exit_app.pack(fill="x", pady=5)
    exit_app.bind("<Enter>", lambda e: on_hover(e, exit_app))
    exit_app.bind("<Leave>", lambda e: on_leave(e, exit_app))
    exit_app.bind("<Button-1>", lambda e: root.destroy())

    # "About" Option
    about = Label(
        menu_popup,
        text="About",
        font=menu_font,
        bg=normal_bg,
        fg=text_color,
        anchor="w",
        padx=10
    )
    about.pack(fill="x", pady=5)
    about.bind("<Enter>", lambda e: on_hover(e, about))
    about.bind("<Leave>", lambda e: on_leave(e, about))
    about.bind("<Button-1>", lambda e: messagebox.showinfo("About", "Show app information"))

    # Close the menu if clicked outside
    menu_popup.bind("<FocusOut>", lambda e: close_menu(menu_popup))
    root.bind("<Button-1>", lambda e: close_menu(menu_popup), add="+")

def add_logo(canvas, logo_path, x=10, y=10):
    """
    Add a logo to the canvas at the specified position.
    
    Parameters:
    canvas (Canvas): The canvas where the logo will be placed.
    logo_path (str): The path to the logo image file.
    x (int): X-coordinate for placing the logo.
    y (int): Y-coordinate for placing the logo.
    """
    try:
        # Load and resize the logo image
        logo_image = Image.open(logo_path).resize((150, 50), Image.ANTIALIAS)
        logo_image = logo_image.convert("RGBA")  # Ensure the image supports transparency
        data = logo_image.getdata()

        # Replace white background with transparency
        new_data = [
            (255, 255, 255, 0) if item[0] > 200 and item[1] > 200 and item[2] > 200 else item
            for item in data
        ]
        logo_image.putdata(new_data)
        logo_photo = ImageTk.PhotoImage(logo_image)

        # Add the logo to the canvas
        canvas.create_image(x, y, anchor=tk.NW, image=logo_photo)
        canvas.logo_image = logo_photo  # Keep a reference to avoid garbage collection
    except FileNotFoundError:
        print(f"Logo image not found: {logo_path}")
