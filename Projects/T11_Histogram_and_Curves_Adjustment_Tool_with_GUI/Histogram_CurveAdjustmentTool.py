#!/usr/bin/env python
# coding: utf-8

# In[20]:



# In[ ]:


import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt

# Function to load an image file
def load_image():
    global img, img_tk, original_img, canvas
    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg;*.bmp")])
    if file_path:
        # Read and convert the image from BGR to RGB
        original_img = cv2.imread(file_path)
        original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
        img = original_img.copy()
        display_image(img)  # Display the loaded image
        update_histogram()  # Update the histogram

# Function to save the adjusted image
def save_image():
    global img
    # Open save file dialog to specify file name and format
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg;*.bmp")])
    if file_path:
        # Convert image back to BGR and save it
        save_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(file_path, save_img)

# Function to display an image on the canvas
def display_image(image):
    global img_tk, canvas
    # Resize image to fit within the canvas
    img_resized = cv2.resize(image, (400, 400))
    # Convert the image to a PIL Image and then to ImageTk format
    img_pil = Image.fromarray(img_resized)
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

# Function to calculate and display the histogram
def update_histogram():
    global img
    # Calculate histograms for each color channel
    hist_r = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([img], [1], None, [256], [0, 256])
    hist_b = cv2.calcHist([img], [2], None, [256], [0, 256])

    # Plot the histograms using Matplotlib
    plt.figure(figsize=(6, 4))
    plt.plot(hist_r, color='r', label='Red')
    plt.plot(hist_g, color='g', label='Green')
    plt.plot(hist_b, color='b', label='Blue')
    plt.legend()
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.title('Histogram')

    # Save the histogram plot as an image
    plt.tight_layout()
    plt.savefig('histogram_temp.png')
    plt.close()

    # Display the histogram image on the canvas
    hist_img = Image.open('histogram_temp.png')
    hist_img.thumbnail((400, 200))
    hist_tk = ImageTk.PhotoImage(hist_img)

    hist_canvas.create_image(0, 0, anchor=tk.NW, image=hist_tk)
    hist_canvas.image = hist_tk

# Function to apply brightness and contrast adjustments
def apply_curves():
    global img
    # Get brightness (alpha) and contrast (beta) values from sliders
    alpha = brightness_slider.get()
    beta = contrast_slider.get()
    
    # Adjust the image using OpenCV's convertScaleAbs function
    adjusted = cv2.convertScaleAbs(original_img, alpha=alpha, beta=beta)
    img = adjusted  # Update the global image variable
    display_image(img)  # Display the adjusted image
    update_histogram()  # Update the histogram

# Function to reset the image to its original state
def reset_image():
    global img
    img = original_img.copy()  # Restore the original image
    display_image(img)  # Display the original image
    update_histogram()  # Update the histogram

# Initialize main GUI window
root = tk.Tk()
root.title("Histogram and Curves Adjustment GUI")

# Create frames for layout
frame_top = tk.Frame(root)
frame_top.pack(side=tk.TOP, pady=10)

frame_image = tk.Frame(root)
frame_image.pack(side=tk.LEFT, padx=10, pady=10)

frame_controls = tk.Frame(root)
frame_controls.pack(side=tk.RIGHT, padx=10, pady=10)

frame_hist = tk.Frame(root)
frame_hist.pack(side=tk.BOTTOM, pady=10)

# Canvas for displaying the image
canvas = tk.Canvas(frame_image, width=400, height=400, bg="gray")
canvas.pack()

# Canvas for displaying the histogram
hist_canvas = tk.Canvas(frame_hist, width=400, height=200, bg="white")
hist_canvas.pack()


# Create the label for the brightness scale
brightness_label = ttk.Label(frame_controls, text="Brightness")
brightness_label.pack()

# Create the brightness slider
brightness_slider = ttk.Scale(frame_controls, from_=0.5, to=2.0, value=1.0, orient=tk.HORIZONTAL, length=200)
brightness_slider.pack()

# Create the label for the contrast scale
contrast_label = ttk.Label(frame_controls, text="Contrast")
contrast_label.pack()

# Create the contrast slider
contrast_slider = ttk.Scale(frame_controls, from_=0, to=100, value=0, orient=tk.HORIZONTAL, length=200)
contrast_slider.pack(pady=5)



# Buttons for applying adjustments, resetting, and saving
apply_button = ttk.Button(frame_controls, text="Apply Curves", command=apply_curves)
apply_button.pack(pady=5)

reset_button = ttk.Button(frame_controls, text="Reset", command=reset_image)
reset_button.pack(pady=5)

save_button = ttk.Button(frame_controls, text="Save Image", command=save_image)
save_button.pack(pady=5)

# Menu for loading images and exiting the application
menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Load Image", command=load_image)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Run the application
root.mainloop()


# In[ ]:




