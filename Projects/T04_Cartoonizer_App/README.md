# Cartoonizer App

## Overview
The Cartoonizer App is a MATLAB-based graphical user interface (GUI) tool that allows users to transform an image into a cartoon-like representation. Users can upload an image, adjust edge thickness, and control color quantization to customize the cartoon effect.
This app was developed by Mohammad Shehroz Ashraf & Syeda Beena Rizvi as part of their Final CAP 5405 - Digital Image Processing Project.
## Features
- **Upload Image**: Supports image files in `.jpg`, `.png`, and `.jpeg` formats.
- **Edge Thickness Control**: Use a slider with discrete steps (1 to 5) to adjust the thickness of edges in the cartoon effect.
- **Color Quantization**: Choose the number of quantization levels (8, 16, 32, or 64) to control the cartoon color palette.
- **Preview Panels**: Displays the original image and the cartoonized result side by side.

## Requirements
- MATLAB R2019b or later (required for `uifigure` and modern GUI components).
- Image Processing Toolbox.

## How to Run the App
1. **Open MATLAB**:
   Make sure you have MATLAB installed on your device and all the required toolboxes.

2. **Save the Script**:
   Save the provided `cartoonizeAppFinal.m` file in your working directory.

3. **Run the Script**:
   - Navigate to the directory containing `cartoonizeAppFinal.m` in MATLAB.
   - Type `cartoonizeAppFinal` in the Command Window and press Enter.

4. **Launch the GUI**:
   The Cartoonizer App will open in a new window.

## Using the GUI
### Step-by-Step Detailed Instructions
1. **Upload an Image**:
   - Click on the `Upload Image` button.
   - Select a supported image file (`.jpg`, `.png`, `.jpeg`) from your computer.
   - The image will be displayed in the left preview panel.

2. **Adjust Edge Thickness**:
   - Use the `Edge Size` slider to set the thickness of the edges.
   - The slider has five discrete options: 1, 2, 3, 4, and 5.

3. **Set Color Quantization**:
   - Select the number of colors from the `Color Quantization` dropdown menu.
   - Options include 8, 16, 32, and 64 colors.

4. **Apply Cartoon Effect**:
   - Click the `Cartoonize` button to generate the cartoonized image.
   - The cartoonized image will be displayed in the right preview panel.

## Notes
- **Image Requirements**:
  - The app supports RGB images. If the uploaded image includes an alpha channel, it will be automatically removed.
  - Ensure the image file is not corrupted or unsupported.

- **Customizations**:
  - Experiment with different edge thickness and color quantization levels to achieve the desired cartoon effect.

- **Errors**:
  - If an invalid file format is uploaded, an alert will notify the user.
  - Ensure the Image Processing Toolbox is installed if you encounter issues.

## Contact
For any sort of issues or to request using our developed app, please contact: mashraf2023@fau.edu or srizvi2024@fau.edu .

