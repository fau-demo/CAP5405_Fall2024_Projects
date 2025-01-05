# Digital_Image_Processing
Histogram and curve adjustment tool using GUI
## Team members:  Tejasri koleti
# Histogram and Curves Adjustment GUI

This project is a Python-based GUI application for visualizing and manipulating images by adjusting their brightness and contrast. It also displays the image histogram, allowing users to analyze the pixel distribution.

## Features
- Load images of various formats (`.jpg`, `.png`, `.jpeg`, `.bmp`).
- Adjust brightness and contrast interactively using sliders.
- View updated histograms for real-time changes.
- Save the modified image to the desired location.
- Reset the image to its original state.

## Prerequisites
1. **Operating System**: Compatible with Windows, macOS, and Linux.
2. **Python Version**: Python 3.7 or higher.
3. **Required Libraries**:
   - `tkinter` (included with Python by default).
   - `opencv-python-headless`: For image manipulation.
   - `Pillow`: For handling images in Python.
   - `matplotlib`: For plotting histograms.

Install the required libraries using:
```bash
pip install opencv-python-headless pillow matplotlib

## How to Run the Program
1. Clone this repository or download the script.
2. Save the script as histogram_curves_gui.py.
3. Open a terminal or command prompt, navigate to the directory containing the script, and run:
python histogram_curves_gui.py
4. A GUI window will open, allowing you to load and process images.

## How to Use the GUI
1. **Load Image**:
   - Go to the menu: `File > Load Image`.
   - Select an image file from your system. Supported formats are `.jpg`, `.png`, `.jpeg`, and `.bmp`.

2. **Adjust Brightness and Contrast**:
   - Use the brightness slider to adjust the overall brightness (`0.5` to `2.0` range, default `1.0`).
   - Use the contrast slider to modify the image contrast (`0` to `100` range, default `0`).
   - Click **Apply Curves** to apply the changes.

3. **Reset Image**:
   - Click the **Reset** button to revert the image to its original state.

4. **Save Image**:
   - Click the **Save Image** button to save the modified image.


## Input Image Details
- **Formats Supported**: `.jpg`, `.png`, `.jpeg`, `.bmp`.

- **Recommended Size**: For optimal performance, use images smaller than 5 MB.

- **Output Format**: Saved images default to `.png` unless another format is specified during saving.

## Expected Output
- The GUI displays:
  - The loaded image on a 400x400 canvas.
  - It's histogram below the image.
  - Brightness and contrast sliders for interactive adjustments.
- The modified image and histogram are updated in real-time based on slider adjustments.


## References
1. [Python Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
2. [OpenCV Python Documentation](https://docs.opencv.org/)
3. [Matplotlib Documentation](https://matplotlib.org/stable/index.html)
