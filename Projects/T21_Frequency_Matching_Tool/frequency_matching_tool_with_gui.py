# -*- coding: utf-8 -*-
"""Frequency matching Tool with GUI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QTfogpIELny3eX1rMNoF-X026NGev06G
"""

import zipfile
import os

'''
# List of zip files to unzip
zip_files = ["dataset.zip", "logs.zip"]

# Loop through each zip file and extract
for zip_file in zip_files:
    extract_dir = zip_file.replace(".zip", "_extracted")  # Create a folder based on the zip file name
    os.makedirs(extract_dir, exist_ok=True)  # Ensure the folder exists
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)  # Extract contents
    print(f"Files from {zip_file} have been extracted to {extract_dir}")
'''


import gradio as gr
import cv2 as cv
import os
import numpy as np
from scipy.signal import spectrogram, stft, windows
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Resize and pad function
def resize_and_pad(image, target_size=(256, 256), pad_color=0):
    height, width = image.shape[:2]
    target_width, target_height = target_size
    scaling_factor = min(target_width / width, target_height / height)
    new_width = int(scaling_factor * width)
    new_height = int(scaling_factor * height)
    resized = cv.resize(image, (new_width, new_height), interpolation=cv.INTER_AREA)
    top_pad = (target_height - new_height) // 2
    bottom_pad = target_height - new_height - top_pad
    left_pad = (target_width - new_width) // 2
    right_pad = target_width - new_width - left_pad
    padded = cv.copyMakeBorder(resized, top_pad, bottom_pad, left_pad, right_pad, cv.BORDER_CONSTANT, value=pad_color)
    return padded

### Image Preprocessing script, no need to run this in real time

# def preprocess_images(input_folder, output_folder, size):
#     """
#     Preprocess images by converting them to grayscale, resizing and padding.

#     Args:
#         input_folder (str): Orginal dataset folder.
#         output_folder (str): Path for saving the preprocessed images.
#         size (tuple): New Target size for resized images.
#     """

#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)


#     for root, dirs, files in os.walk(input_folder):

#         relative_path = os.path.relpath(root, input_folder)
#         output_subfolder = os.path.join(output_folder, relative_path)

#         if not os.path.exists(output_subfolder):
#             os.makedirs(output_subfolder)

#         for file_name in files:
#             if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):

#                 file_path = os.path.join(root, file_name)
#                 img = cv.imread(file_path)

#                 if img is None:
#                     print(f"Error loading image: {file_path}")
#                     continue

#                 resized = resize_and_pad(img, target_size=size) ## resizing all images to standard size of 256x256
#                 gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)


#                 output_path = os.path.join(output_subfolder, file_name)
#                 cv.imwrite(output_path, gray)

#                 print(f"Processed: {file_path} -> {output_path}")

# Compute 2D STFT spectrogram
def compute_spectrogram(image, window_size=32, overlap=0.5, window_type="hann"):
    image = image / 255.0  # Normalize
    step = int(window_size * (1 - overlap))
    rows, cols = image.shape
    aggregated_magnitude = np.zeros((rows, cols))
    weights = np.zeros_like(aggregated_magnitude)
    if window_type == "hann":
        window = windows.hann(window_size)
    elif window_type == "gaussian":
        window = windows.gaussian(window_size, std=window_size / 6)
    elif window_type == "boxcar":
        window = windows.boxcar(window_size)
    else:
        raise ValueError("Unsupported window type")
    window_2d = np.outer(window, window)
    for i in range(0, rows - window_size + 1, step):
        for j in range(0, cols - window_size + 1, step):
            region = image[i : i + window_size, j : j + window_size]
            region_windowed = region * window_2d
            region_fft = np.fft.fft2(region_windowed)
            region_magnitude = np.abs(np.fft.fftshift(region_fft))
            aggregated_magnitude[i : i + window_size, j : j + window_size] += region_magnitude
            weights[i : i + window_size, j : j + window_size] += window_2d
    aggregated_magnitude /= np.maximum(weights, 1e-8)
    return aggregated_magnitude

# Match spectrograms
def match_spectrograms(s1, s2, method="pearson"):
    s1 = s1 / np.max(s1)
    s2 = s2 / np.max(s2)
    if method == "ssim":
        correlation = ssim(s1, s2, data_range=1.0)
    elif method == "pearson":
        correlation = np.corrcoef(s1.flatten(), s2.flatten())[0, 1]
    else:
        raise ValueError("Unsupported method")
    return round(correlation, 3)

# Display image and spectrogram
def generate_spectrogram_image(image, title="Spectrogram"):
    plt.figure(figsize=(4, 4))
    plt.imshow(np.log(1 + image), cmap="viridis", aspect="auto")
    plt.title(title)
    plt.axis("off")
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight", pad_inches=0)
    buffer.seek(0)
    plt.close()
    return Image.open(buffer)

# Main Gradio Functionality
def frequency_matching(target_image_path, dataset_folder, top_n=3):
    target_image = cv.imread(target_image_path, cv.IMREAD_GRAYSCALE)
    if target_image is None:
        raise ValueError("Could not load target image")
    target_image_resized = resize_and_pad(target_image, target_size=(256, 256))
    target_spectrogram = compute_spectrogram(target_image_resized)

    results = []
    for root, _, files in os.walk(dataset_folder):
        for file_name in files:
            if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                file_path = os.path.join(root, file_name)
                dataset_image = cv.imread(file_path, cv.IMREAD_GRAYSCALE)
                if dataset_image is None:
                    continue
                dataset_image_resized = resize_and_pad(dataset_image, target_size=(256, 256))
                dataset_spectrogram = compute_spectrogram(dataset_image_resized)
                correlation = match_spectrograms(target_spectrogram, dataset_spectrogram)
                results.append((file_path, correlation))



    results = sorted(results, key=lambda x: x[1], reverse=True)[:top_n]

    # Prepare outputs
    spectrogram_image = generate_spectrogram_image(target_spectrogram, "Target Spectrogram")
    matches = [(res[0], generate_spectrogram_image(compute_spectrogram(cv.imread(res[0], cv.IMREAD_GRAYSCALE)), f"Match {i+1}"), res[1]) for i, res in enumerate(results)]
    return spectrogram_image, matches

def display_matches(target_image, top_n):
    """
    Processes the target image, matches it against the dataset, and returns results.

    Args:
        target_image (str): Path to the target image.
        top_n (int): Number of top matches to return.

    Returns:
        tuple: Target spectrogram image and a list of match images with captions.
    """
    dataset_folder = "./dataset/preprocessed_data/natural_images"
    spectrogram_image = generate_spectrogram_image(
        compute_spectrogram(cv.imread(target_image, cv.IMREAD_GRAYSCALE)),
        title="Target Spectrogram"
    )

    # Perform matching
    _, matches = frequency_matching(target_image, dataset_folder, top_n)

    results = []
    for match in matches:
        match_image = cv.imread(match[0], cv.IMREAD_COLOR)
        match_image = cv.cvtColor(match_image, cv.COLOR_BGR2RGB)  # Convert to RGB for display
        match_image = Image.fromarray(match_image)

        match_spectrogram = generate_spectrogram_image(
            compute_spectrogram(cv.imread(match[0], cv.IMREAD_GRAYSCALE)),
            title="Match Spectrogram"
        )

        # Concatenate match image and spectrogram horizontally
        combined_image = Image.new("RGB", (match_image.width + match_spectrogram.width, match_image.height))
        combined_image.paste(match_image, (0, 0))
        combined_image.paste(match_spectrogram, (match_image.width, 0))

        # Add combined image and caption to results
        caption = f"Correlation: {match[2]}"
        results.append((combined_image, caption))

    return spectrogram_image, results

input_image = gr.Image(label="Upload Target Image", type="filepath")
num_matches = gr.Slider(minimum=1, maximum=10, value=3, step=1, label="Number of Matches")
spectrogram_output = gr.Image(label="Target Spectrogram")
matches_output = gr.Gallery(label="Top Matches (Image + Spectrogram + Correlation)")

iface = gr.Interface(
    fn=display_matches,
    inputs=[input_image, num_matches],
    outputs=[spectrogram_output, matches_output],
    title="Frequency Matching Tool",
    description="Upload an image to find spectrogram matches.",
)

iface.launch(share=True)

