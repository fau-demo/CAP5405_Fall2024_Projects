#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import cv2
import matplotlib.pyplot as plt
import numpy as np


# In[2]:


image_directory= "C:/Users/vaish/Desktop/SEM3/TA/CAP5405_Fall2024_Projects/T14_Background_Removal_from_Scanned_Facades_in_Python/Background Removal/Input"
output = "C:/Users/vaish/Desktop/SEM3\TA/CAP5405_Fall2024_Projects/T14_Background_Removal_from_Scanned_Facades_in_Python/Background Removal/Output"


# In[ ]:


def remove_background_with_plot(image_path, save_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error loading image: {image_path}")
        return

    # Convert to RGB 
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert to grayscale
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply threshold to create a binary mask
    _, mask = cv2.threshold(grayscale, 200, 255, cv2.THRESH_BINARY)

    # Invert the mask to identify the foreground
    inverted_mask = cv2.bitwise_not(mask)

    # Create a 4-channel (RGBA) image for transparency
    background_removed = cv2.merge((image[:, :, 0], image[:, :, 1], image[:, :, 2], inverted_mask))

    # Save the processed image with transparency
    saved = cv2.imwrite(save_path, background_removed)
    if saved:
        print(f"Image saved successfully to: {save_path}")
    else:
        print(f"Failed to save image to: {save_path}")

    # Prepare for plotting
    
    # Convert background-removed image (RGBA needs normalization to 0-1)
    background_removed_for_plot = background_removed.astype(np.float32) / 255.0

    # Plot the steps
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    axes[0].imshow(image_rgb)
    axes[0].set_title("Original Image")
    axes[0].axis('off')

    axes[1].imshow(grayscale, cmap='gray')
    axes[1].set_title("Grayscale Image")
    axes[1].axis('off')

    axes[2].imshow(mask, cmap='gray')
    axes[2].set_title("Binary Mask")
    axes[2].axis('off')

    axes[3].imshow(background_removed_for_plot)
    axes[3].set_title("Transparent Background")
    axes[3].axis('off')

    plt.tight_layout()
    plt.show()


os.makedirs(output, exist_ok=True)

# Process and plot each image
for filename in os.listdir(image_directory):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        input_path = os.path.join(image_directory, filename)
        output_path = os.path.join(output, filename)

        # Ensure output file has .png extension for transparency
        if not output_path.lower().endswith('.png'):
            output_path = os.path.splitext(output_path)[0] + '.png'

        print(f"Processing file: {input_path}")
        remove_background_with_plot(input_path, output_path)

print(f"All images processed. Check the output folder: {output}")


# In[7]:


def calculate_psnr_result(processed):

    # Create a reference image of the same shape with all transparent background
    reference = np.zeros_like(processed, dtype=processed.dtype)

    # Compute the Mean Squared Error (MSE) only on RGB channels
    processed_rgb = processed[:, :, :3]
    reference_rgb = reference[:, :, :3]
    mse = np.mean((processed_rgb - reference_rgb) ** 2)
    if mse == 0:
        return float('inf') 

    # Calculate PSNR
    max_pixel = 255.0
    psnr_value = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr_value


# In[9]:


output= "C:/Users/skatsangelou2023/Documents/ELL/facades_sunday"

# Calculate PSNR for each image in the output directory
psnr_results = {}
for filename in os.listdir(output):
    if filename.lower().endswith('.png'):  # Ensure only .png files are processed
        output_path = os.path.join(output, filename)
        
        # Load the processed image
        processed = cv2.imread(output_path, cv2.IMREAD_UNCHANGED)  # Load RGBA
        
        if processed is not None:
            # Calculate PSNR
            psnr_value = calculate_psnr_result(processed)
            psnr_results[filename] = psnr_value
            print(f"PSNR for {filename}: {psnr_value:.2f} dB")
        else:
            print(f"Failed to load {filename}")


# In[11]:


import statistics
psnr_values = list(psnr_results.values())
if psnr_values:
    median_psnr = statistics.median(psnr_values)
    print(f"\nMedian PSNR for all images: {median_psnr:.2f} dB")
else:
    print("\nNo PSNR values were calculated. Check the output folder and image processing.")


# Peak signal-to-noise ratio (PSNR) is a measure of the quality of a signal or image by comparing the maximum power of a signal to the power of corrupting noise. A PSNR of 30db or above is considered a good ratio and indicates high similarity between the images. Minimal distortion or loss of quality.
