
# Project title: Image Editing Tool (Histogram and curves adjustment GUI)


# Team Members
# Sai Sampath Reddy Goli - Z23754767
# Kommuri Hari Krishna - Z23741299 


This is a Python-based GUI application for image editing, built with Tkinter and OpenCV. The tool allows users to make adjustments to images, such as brightness, contrast, and color balance, as well as resize and save the edited images.

## Features

- **Brightness and Contrast Adjustments:** Dynamically adjust the brightness and contrast of the image.
- **Color Balance:** Adjust red, green, and blue channels to enhance image color tones.
- **Resize Images:** Resize the image to a specified percentage of the original size.
- **Reset Edits:** Reset all adjustments to restore the original image.
- **Save Edited Image:** Save the final edited image in JPG or PNG format.


## Software used

Before running the application, make sure you have the following installed:

- Python 3.x
- Required Python libraries:
  - OpenCV (`cv2`)
  - NumPy
  - Tkinter (comes pre-installed with Python)
  - Pillow (`PIL`)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/sampathgoli/DIP-Project.git
   

   ```

2. **Install Dependencies:**
   Install the required Python libraries using pip:
   ```bash
   pip install opencv-python 
   pip install opencv-python-headless
   pip install opencv-numpy 
   pip install opencv-pillow
   ```

## How to Run

1. Navigate to the project folder where the script is located.
2. Run the Python script:
   ```bash
   python image_editor_gui.py
   ```

3. The GUI application will open. From there, you can:
   - Load an image file.
   - Adjust brightness, contrast, and color balance using sliders.
   - Resize the image.
   - Save the edited image.

## User Interface Overview

1. **Load Image:**
   - Click the "Load Image" button to open an image file (supported formats: `.jpg`, `.png`).

2. **Adjustments:**
   - Use sliders to modify brightness, contrast, and color balance.
   - Resize the image using the "Resize Image (%)" slider.

3. **Reset Edits:**
   - Click the "Reset" button to undo all adjustments and restore the original image.

4. **Save Image:**
   - Click the "Save" button to save the edited image. You can select the format (`.jpg` or `.png`) and location.

## Project Structure

```
.
├── README.md             # Project documentation
├── image_editor_gui.py # Main Python script
```

## Expected Output
1. After loading an image, you will see two canvases: one showing the original image and another showing the edited image.
2. You can adjust the brightness, contrast, and color balance (RGB sliders).
3. After resizing, both images (original and edited) will reflect the updated size.
4. Once the image adjustments are made, you can save the final image in .jpg or .png format.

## Input Image Format and Size
1. Supported Formats: .jpg, .png
2. Input Image Size: The tool supports any image size, but very large images may take longer to process.
3. Aspect Ratio: The program maintains the aspect ratio when resizing the image.

## Operating System Compatibility

1. Windows
2. macOS
3. Linux
4. Us

## References & Resources
1. OpenCV: Official documentation for OpenCV - https://opencv.org/
2. Tkinter: Official Python documentation for Tkinter - https://docs.python.org/3/library/tkinter.html
3. Pillow (PIL): Official documentation for Pillow - https://pillow.readthedocs.io/en/stable/


