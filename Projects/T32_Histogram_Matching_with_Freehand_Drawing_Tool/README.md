# Histogram Matching with Freehand Drawing Tool

## Team Members
- Sathwik Mallavarapu

## Software Used
- **Operating Systems**: Windows
- **Programming Language:** Python
- **GUI Framework:** Tkinter
- **Image Processing Libraries:** OpenCV, PIL (Pillow)
- **Development Environment:** Visual Studio Code

## Project Overview
This project focuses on the development of a Python-based graphical user interface (GUI) application for interactive image processing, specifically targeting histogram matching. Histogram matching adjusts the color distribution of one image to resemble that of another. This application features a freehand drawing tool, enabling users to intuitively mark areas for localized histogram matching.

### Key Features
- **Freehand Drawing Tool**: Allows users to sketch directly on the image for localized processing.
- **Histogram Matching**: Real-time color distribution adjustment using OpenCV's LAB color space.
- **Basic Image Editing**: Supports image loading, drawing, clearing, and exporting results.
- **User-Friendly Interface**: Provides responsive and intuitive buttons for seamless operation.

## Functional Requirements
1. **Load and Display Images**
   - Load a target and reference image from local storage.
   - Display both images within the GUI.
   
2. **Freehand Drawing Tool**
   - Draw directly on the image to select regions for processing.
   - Options to clear/reset drawings.

3. **Histogram Matching**
   - Match the histogram of the user-selected region with the reference image.
   - Apply real-time adjustments for instant feedback.

4. **Export Results**
   - Save the processed image to the local system in supported formats (e.g., JPG, PNG).

5. **User Interface**
   - Intuitive design with clear buttons for loading, drawing, resetting, and exporting.


## Installation Guide
1. Clone this repository:
   ```bash
   git clone [https://github.com/SathwikMallavarapu/Histogram-Matching-with-Freehand-Drawing-Tool](https://github.com/SathwikMallavarapu/Histogram-Matching-with-Freehand-Drawing-Tool.git)
   cd histogram-matching-tool

## Install dependencies:
opencv-python==4.5.5.64, 
Pillow==8.4.0,
numpy==1.21.5, 
matplotlib==3.5.1, 

## Run the application:
python main.py

## Expected Output
**Input**: Images in PNG or JPG formats with dimensions up to 1920x1080.
**Output**: Processed images with localized histogram-matched sections in the same format as input.

## References and Resources
- The project uses OpenCV's LAB color space for accurate histogram matching.
- References to libraries and concepts are cited in the code comments.
- Additional resources can be found in the `References.md` file (included in this repository).


## Comments and Documentation
The code is well-commented for readability and understanding.
A step-by-step guide for usage is included within the `help.md` file.

## Future Scope
Add advanced image filters such as sharpening and blurring.
Enable batch processing for multiple images simultaneously.
Integrate with cloud storage platforms for saving and retrieving images.

**Contact:**  
For questions or feedback, please contact us at [Tikusathwik@gmail.com].
