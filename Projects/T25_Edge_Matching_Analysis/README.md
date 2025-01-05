# Edge Detection Analysis Tool

# Team Members
Satyajyothi Achanta - Z23709570
Manikanta Swamy Yedla - Z23709569
Abhiram Reddy Neboori - Z23749867

## Overview
This tool implements edge detection algorithms for image retrieval using MATLAB and Python. It supports multiple datasets and provides a user-friendly GUI for non-technical users.

The Edge Detection Analysis Tool implements edge detection algorithms for image retrieval using MATLAB and Python. This tool is designed to support multiple datasets and provides a user-friendly graphical user interface (GUI) for non-technical users, enabling them to experiment with various edge detection algorithms.

## Features
- **Edge Detection Algorithms:** Canny, Sobel, Prewitt, Adaptive Canny, Multi-Scale Detection.
- **Profile Comparison:** SSIM and correlation metrics for accuracy evaluation.
- **GUI:** Allows easy interaction and real-time parameter adjustment.

## Installation
### Requirements
- Python 3.9 or higher / Jupyter Notebook
- MATLAB R2021b or later
- Libraries: OpenCV, NumPy, scikit-image, Pillow

### Instructions
1. Clone this repository: `git clone <repository-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch:
   - MATLAB: Open and run `EdgeDetectionTool.m`
   - Python: Run `python main.py`

## Usage
1. Load an image via the GUI:
   Use the provided interface to select an image from your local system. Ensure the image is in an appropriate format (JPG, PNG, BMP).
2. Select an edge detection algorithm:
   Choose between Canny, Sobel, Prewitt, Adaptive Canny, or Multi-Scale Detection.
3. Adjust the parameters:
   For each algorithm, you can adjust various parameters, such as thresholds for edge detection and scaling factors.
4. View and save the results:
   The results will be displayed on the interface in real-time.

## Input Images
Supported Formats: JPG, PNG, BMP
Recommended Size: Images should not exceed 5000x5000 pixels for optimal performance. Larger images may result in longer processing times.

## Operating System Support
Windows: The tool is fully supported on Windows 10 or later.
Linux: The tool is compatible with most distributions, including Ubuntu and Fedora.
macOS: Support for macOS is available but not fully tested.

## Expected Output
Edge-detected Image: The output image will highlight the detected edges, based on the selected algorithm.
Profile Metrics: SSIM (Structural Similarity Index) and correlation metrics will be displayed, allowing for accuracy comparison between different algorithms or ground truth images.

## References
1.	Canny, J. (1986). A computational approach to edge detection. IEEE Transactions on Pattern Analysis and Machine Intelligence, 8(6), 679-698.
2.	Jähne, B. (2005). Digital image processing: concepts, algorithms, and applications. Springer Science & Business Media.
3.	Gonzalez, R. C., & Woods, R. E. (2018). Digital Image Processing. Pearson.
4.	OpenCV Documentation. Available at: https://docs.opencv.org/
5.	MathWorks MATLAB Documentation. Available at: https://www.mathworks.com/help/matlab/

## Datasets
- henryscheible_coco_val2014_tiny
- theodor1289_imagenet-1k_tiny
