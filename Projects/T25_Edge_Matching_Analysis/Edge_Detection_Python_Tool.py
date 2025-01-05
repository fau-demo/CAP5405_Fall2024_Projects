import tkinter as tk
from tkinter import Toplevel, filedialog, Label, Frame, StringVar
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="PIL.Image")

# Global variables
img = None
detected_edges = None

# Adaptive thresholding for Canny
def adaptive_canny(img):
    mean_val = np.mean(img)
    lower = max(0, int(0.66 * mean_val))  # Lower threshold
    upper = min(255, int(1.33 * mean_val))  # Upper threshold
    return cv2.Canny(img, lower, upper)

# Multi-scale edge detection
def multi_scale_edges(img, method):
    scales = [0.5, 1.0, 1.5]
    edges_sum = np.zeros_like(img, dtype=np.float32)
    for scale in scales:
        resized = cv2.resize(img, (0, 0), fx=scale, fy=scale)
        edges = detect_edges(resized, method)
        edges = cv2.resize(edges, (img.shape[1], img.shape[0]))  # Resize back to original
        edges_sum += edges
    edges_combined = np.uint8(edges_sum / len(scales))
    return edges_combined

# Noise reduction
def noise_reduction(img):
    blurred = cv2.GaussianBlur(img, (5, 5), 0)  # Gaussian Blur
    return blurred

# Edge detection with advanced options
def detect_edges(img, method):
    img = noise_reduction(img)  # Apply noise reduction
    if method == "Sobel":
        sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
        sobel = cv2.magnitude(sobel_x, sobel_y)
        return np.uint8(sobel / np.max(sobel) * 255)
    elif method == "Prewitt":
        kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
        kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
        prewittx = cv2.filter2D(img.astype(np.float32), -1, kernelx)
        prewitty = cv2.filter2D(img.astype(np.float32), -1, kernely)
        prewitt = cv2.magnitude(prewittx, prewitty)
        return np.uint8(prewitt / np.max(prewitt) * 255)
    elif method == "Canny":
        return cv2.Canny(img, 100, 200)  # Standard Canny
    elif method == "Adaptive Canny":
        return adaptive_canny(img)
    elif method == "Multi-Scale":
        return multi_scale_edges(img, "Canny")
    elif method == "Hybrid":
        sobel = detect_edges(img, "Sobel")
        canny = detect_edges(img, "Canny")
        return cv2.addWeighted(sobel, 0.5, canny, 0.5, 0)
    else:
        return img

# Select and process an image
def open_image():
    global img, detected_edges
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        img = cv2.imread(file_path)#, cv2.IMREAD_GRAYSCALE)
        detected_edges = None  # Reset edges when a new image is loaded
        display_image(img, img_panel)
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        display_image(None, edge_panel)  # Clear the right panel

# Apply edge detection
def apply_edge_detection():
    global detected_edges
    if img is None:
        return
    selected_method = edge_detection_var.get()
    detected_edges = detect_edges(img, selected_method)
    display_image(detected_edges, edge_panel)

# Find similar images
def find_similar_images():
    global detected_edges
    if img is None:
        print("Please load an image before finding similar images.")
        return
    if detected_edges is None:
        print("Please apply edge detection before finding similar images.")
        return

    folder_path = filedialog.askdirectory(title="Select Dataset Folder")
    if not folder_path:
        print("No folder selected.")
        return

    # Initialize similarity tracking
    similar_images = []
    list_similarityscore=[] # List to store (image_path, SSIM_score)
    similarity_threshold = 0.55  # Define a similarity threshold
    target_shape = detected_edges.shape  # Shape of the reference edges

    print(f"Analyzing images in folder: {folder_path}")
    for file in os.listdir(folder_path):
        file_full_path = os.path.join(folder_path, file)
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            try:
                dataset_img = cv2.imread(file_full_path, cv2.IMREAD_GRAYSCALE)
                if dataset_img is None:
                    print(f"Skipping unsupported or corrupted file: {file}")
                    continue

                # Resize the dataset image to match the target shape
                dataset_img_resized = cv2.resize(dataset_img, (target_shape[1], target_shape[0]))

                # Perform edge detection on the dataset image
                dataset_edges = detect_edges(dataset_img_resized, edge_detection_var.get())
                if dataset_edges is None:
                    print(f"Edge detection failed for image: {file}")
                    continue

                # Compare similarity using SSIM
                score, _ = ssim(detected_edges, dataset_edges, full=True)
                print(f"SSIM Score for {file}: {score:.2f}")
                
                list_similarityscore.append((file_full_path,score))
                # Debug: Visualize the edges being compared
                # Display the image using matplotlib
                # plt.imshow(cv2.cvtColor(detected_edges, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for proper display
                # plt.axis('off')  # Hide axes
                # plt.show()
                # print(f"Dataset Edges - {file}")
                # plt.imshow(cv2.cvtColor(dataset_edges, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for proper display
                # plt.axis('off')  # Hide axes
                # plt.show()


                if score > similarity_threshold:
                    similar_images.append(file_full_path)

            except Exception as e:
                print(f"Error processing file {file}: {e}")
                continue

    # Sort images based on SSIM score in descending order
    list_similarityscore.sort(key=lambda x: x[1], reverse=True)

    # Select the top N similar images
    top_similar_images = [image_path for image_path, _ in list_similarityscore[:10]]  # Top 10

    # Display similar images
    if top_similar_images:
        display_similar_images(top_similar_images)  # Display up to 10 similar images
    else:
        print("No similar images found.")
# Display similar images in a new window
def display_similar_images(similar_images):
    similar_window = Toplevel(root)
    similar_window.title("Similar Images")
    similar_window.geometry("800x600")
    similar_window.configure(padx=10, pady=10)

    for idx, path in enumerate(similar_images):
        img = Image.open(path)
        img.thumbnail((200, 200))  # Resize thumbnail for display
        img_tk = ImageTk.PhotoImage(img)

        label = Label(similar_window, image=img_tk)
        label.image = img_tk
        label.grid(row=idx // 3, column=idx % 3, padx=5, pady=5)

    similar_window.mainloop()

# Utility to display an image in a label
def display_image(image, panel):
    if image is None:
        panel.configure(image=None)
        panel.image = None
        return
    image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB) if len(image.shape) == 2 else image
    image_pil = Image.fromarray(image_rgb)
    image_tk = ImageTk.PhotoImage(image_pil)
    panel.configure(image=image_tk)
    panel.image = image_tk

# Create the GUI
def create_gui():
    global root, img_panel, edge_panel, edge_detection_var

    root = tk.Tk()
    root.title("Advanced Edge Detection Tool")
    root.geometry("1000x800")  # Adjust window size

    # Main container frames
    top_frame = Frame(root, padx=10, pady=10)
    top_frame.pack(side="top", fill="x")  # Contains buttons

    image_frame = Frame(root, padx=10, pady=10)
    image_frame.pack(side="top", fill="both", expand=True)  # Contains images

    # Buttons in top_frame
    edge_detection_var = StringVar(value="Canny")
    tk.OptionMenu(top_frame, edge_detection_var, "Canny", "Sobel", "Prewitt", "Adaptive Canny","Multi-Scale","Hybrid").pack(side="left", padx=5)
    tk.Button(top_frame, text="Open Image", command=open_image).pack(side="left", padx=5)
    tk.Button(top_frame, text="Apply Edge Detection", command=apply_edge_detection).pack(side="left", padx=5)
    tk.Button(top_frame, text="Find Similar Images", command=find_similar_images).pack(side="left", padx=5)

    # Image panels in image_frame
    img_panel = Label(image_frame)
    img_panel.pack(side="left", padx=5, pady=5, expand=True)

    edge_panel = Label(image_frame)
    edge_panel.pack(side="left", padx=5, pady=5, expand=True)

    root.mainloop()

# Run the GUI
create_gui()
