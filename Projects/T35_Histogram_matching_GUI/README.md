# Final-Project-DIP

# Histogram Matching Tool for Image Processing

A Python-based GUI tool for automating histogram matching to align the tonal distributions of images. The tool allows users to load images, apply histogram matching, and visualize the results in real-time.

## Project Title

Histogram Matching Tool for Image Processing

## Team Members' Names

- [Meharaj Basha Shaik]
- [Prathima Avula]

## Software Used

- Python 3.6 or higher
- Libraries: Tkinter, Pillow, Matplotlib, Numpy, OpenCV

## Installation and Execution Guide

### System Requirements

- **Python Version**: Python 3.6 or higher
- **Supported Operating Systems**: Windows/Linux
- **Required Libraries**:
  - Tkinter (for GUI)
  - Pillow (for image processing)
  - Matplotlib (for histogram visualization)
  - Numpy (for numerical computations)
  - OpenCV (for image manipulation)

### Installation Steps

1. **Install Python**: Ensure Python 3.6 or higher is installed on your system.  
2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   ```
   Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. **Install Dependencies**:
   ```bash
   pip install pillow matplotlib numpy opencv-python
   ```
4. **Download or Clone the Project**:
   ```bash
   git clone <repository_url>
   ```
   If downloaded as a ZIP, unzip it into your desired folder.

### Execution Steps

1. **Run the Application**:
   ```bash
   python Histogram_Matching_GUI.py
   ```
2. **GUI Usage**:
   - Load images using the "Load Image" and "Load Reference Image" buttons.
   - Perform histogram matching and visualize results.
   - Save the processed image using the "Save Processed Image" button.

### Input Image Requirements

- **Formats**: .jpg, .png, .bmp  
- **Recommended Size**: Under 1920x1080 for better performance.  

### Expected Output

- Processed image with histogram aligned to the reference image.
- Side-by-side display of original, reference, and processed images with their histograms.

## References

- [OpenCV Documentation](https://docs.opencv.org/4.x/index.html)
- [Pillow Documentation](https://pillow.readthedocs.io/en/stable/)
- [Tkinter Python Documentation](https://docs.python.org/3/library/tk.html)
