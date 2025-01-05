from tkinter import filedialog, messagebox
#from editing_screen2 import create_editing_screen
from editing_screen3 import EditingScreen
import os
from PIL import Image, ImageTk
import tkinter as tk

def upload_function(root):
    """
    Opens a file dialog to upload an image and transitions to the editing screen.

    Parameters:
    root (Tk): The main Tkinter root window.
    """
    try:
        # Open a file dialog to select an image
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]  # Supported file formats
        )

        if file_path:  # If the user selects a file
            # Transition to the editing screen with the uploaded image
            #create_editing_screen(root, uploaded_image_path=file_path)  # Alternate function call
            EditingScreen(root, uploaded_image_path=file_path)  # Editing screen creation
        else:
            # Show an info message if no file is selected
            messagebox.showinfo("No File Selected", "Please select an image to proceed.")
    except Exception as e:
        # Handle unexpected errors and display an error message
        messagebox.showerror("Error", f"An error occurred while uploading the image:\n{e}")

def open_gallery_folder(root, folder_path="assets"):
    """
    Opens a specified folder to select an image and transitions to the editing screen.

    Parameters:
    root (Tk): The main Tkinter root window.
    folder_path (str): The folder path to open for gallery images. Defaults to "assets".
    """
    if os.path.exists(folder_path):  # Check if the folder exists
        # Open the folder and allow the user to select an image
        file_path = filedialog.askopenfilename(
            initialdir=folder_path,
            title="Select an Image from Gallery",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]  # Supported file formats
        )
        if file_path:  # If a file is selected
            try:
                # Navigate to the editing screen with the selected image
                #create_editing_screen(root, uploaded_image_path=file_path)  # Alternate function call
                EditingScreen(root, uploaded_image_path=file_path)  # Editing screen creation
            except Exception as e:
                # Handle errors while loading the image and display an error message
                messagebox.showerror("Error", f"Failed to load image.\nError: {e}")
        else:
            # Show a warning if no file is selected
            messagebox.showwarning("No File Selected", "Please select an image to upload.")
    else:
        # Show an error message if the folder does not exist
        messagebox.showerror("Error", f"Folder does not exist: {folder_path}")
