# DIP Project - Sujana Team
**"This project implements edge detection and object segmentation using Python and MATLAB."**

---

# Table of Contents
1. [Introduction](#introduction)
2. [Dataset](#dataset)
3. [Methodology](#methodology)
   - [Python Implementation](#python-implementation)
   - [MATLAB Implementation](#matlab-implementation)
4. [Metrics and Results](#metrics-and-results)
5. [Comparison Between Python and MATLAB](#comparison-between-python-and-matlab)
6. [Challenges and Learnings](#challenges-and-learnings)
7. [Conclusion and Future Work](#conclusion-and-future-work)
8. [How to Run the Code](#how-to-run-the-code)
9. [Requirements](#requirements)

---

## Introduction
This project implements edge detection and object segmentation using **Python** and **MATLAB** to analyze and compare their performance. 

### Objectives:
- Detect edges in images using the **Canny Edge Detection Algorithm**.
- Segment objects from edge-detected images using contours and connected regions.
- Evaluate results using metrics like **Edge Density**, **Mean Gradient Magnitude**, **Number of Objects**, and **Average Object Size**.

The project compares Python and MATLAB's strengths and limitations in handling computer vision tasks, offering insights into their capabilities in image processing workflows.

---

## Dataset
- **Name**: Natural Images Dataset
- **Source**: [Kaggle Natural Images Dataset](https://www.kaggle.com/datasets/prasunroy/natural-images)
- **Size**: 6,899 images
- **Categories**: Airplanes, Cars, People, Flowers, and Buildings

### Preprocessing:
- Images were converted to grayscale to standardize edge detection.
- A subset of 5 images was used for testing and visualization.

---

## Methodology

### Python Implementation
#### **Edge Detection:**
- **Library Used**: OpenCV (`cv2.Canny()`)
- **Metrics Calculated**:
  - **Edge Density**: Ratio of edge pixels to total pixels.
  - **Mean Gradient Magnitude**: Computed using Sobel filters (`cv2.Sobel()`).

#### **Object Segmentation:**
- Extracted contours using `cv2.findContours()`.
- Filtered small contours to remove noise.
- Visualized segmented objects by overlaying green contours on the original images.

**Metrics Calculated:**
- **Number of Objects**
- **Average Object Size**

---

### MATLAB Implementation
#### **Edge Detection:**
- **Function Used**: `edge()` for Canny Edge Detection.
- **Metrics Calculated**:
  - **Edge Density**: Ratio of edge pixels.
  - **Mean Gradient Magnitude**: Computed using Sobel gradients (`imgradientxy`).

# Requirements

## MATLAB Features:
### MATLAB Environment
- Ensure MATLAB is installed with an active license.
- Include the **Image Processing Toolbox** for handling image-related operations.
- Include the **MATLAB Report Generator** for creating PDF reports.

### Toolboxes:
1. **Image Processing Toolbox**
   - Used for functions like `rgb2gray`, `edge`, and image visualization (`imshow`).
   - Required for connected component analysis and edge detection algorithms.
2. **MATLAB Report Generator**
   - Required for generating and saving the PDF report using `mlreportgen.dom`.

## Dataset:
- Images should be in the following formats:
  - `.png`, `.jpg`, `.jpeg`, `.bmp`
- Dataset directory should exist at the specified path and contain properly formatted image files.

## Hardware:
- System with sufficient processing power and memory to handle image analysis operations and large datasets.

## Setup:
1. Ensure the **`natural_images`** dataset is uploaded to your MATLAB Drive path:
   - `/MATLAB Drive/SUJANADIP/natural_images`
2. The output paths for PDF and PNG results should be writable:
   - `/MATLAB Drive/SUJANADIP/edge_detection_analysis_report.pdf`
   - `/MATLAB Drive/SUJANADIP/object_segmentation_results.png`

## Steps for Execution:
1. Load the dataset by ensuring the `folder` variable in the script points to the correct dataset path.
2. Execute the `edge_detection_analysis` function for edge detection.
3. Execute the `object_segmentation_analysis` function for object segmentation.

## MATLAB Online:
If you're running this in **MATLAB Online**:
1. Upload all necessary datasets and scripts to your MATLAB Drive.
2. Verify permissions for generating and saving outputs.


#### **Object Segmentation:**
- Identified connected components using `bwconncomp()`.
- Visualized segmented objects with green contours overlaid on original images.

**Metrics Calculated:**
- **Number of Objects**
- **Average Object Size**

---

## Metrics and Results

### **Edge Detection Metrics:**
- **Edge Density**: Quantifies edge prominence.
- **Mean Gradient Magnitude**: Measures average gradient intensity.

### **Segmentation Metrics:**
- **Number of Objects**: Total objects segmented.
- **Average Object Size**: Mean area of segmented objects.

## How to Run the Code

1. Clone this repository:
   ```bash
   git clone https://github.com/username/dip_project_sujanateam.git
2. Open MATLAB or Python depending on the implementation you wish to run.
3. Follow the appropriate execution steps in the respective folders.
---

### Sample Results (Python)
| Image Name          | Edge Density | Mean Gradient Magnitude | Number of Objects | Average Object Size |
|---------------------|---------------|-------------------------|--------------------|---------------------|
| airplane_0000.jpg   | 0.0403        | 43.2911                | 54                 | 324.40              |
| airplane_0001.jpg   | 0.0385        | 44.5143                | 46                 | 182.50              |

---

### Sample Results (MATLAB)
| Image Name          | Edge Density | Mean Gradient Magnitude | Number of Objects | Average Object Size |
|---------------------|---------------|-------------------------|--------------------|---------------------|
| airplane_0000.jpg   | 0.0398        | 42.8912                | 52                 | 310.20              |
| airplane_0001.jpg   | 0.0379        | 44.3215                | 45                 | 178.90              |

---

## Comparison Between Python and MATLAB

| **Aspect**           | **Python**                         | **MATLAB**                      |
|----------------------|--------------------------------------|----------------------------------|
| Edge Detection       | Flexible, customizable thresholds | Fast with built-in functions   |
| Object Segmentation  | Detected finer details             | Clean segmentation results     |
| Performance          | Handles large datasets effectively| Ideal for rapid prototyping    |
| Visualization        | Requires libraries like Matplotlib | Integrated visualization tools |

---

## Challenges and Learnings

### **Challenges:**
- Handling large datasets in MATLAB Online due to storage limits.
- Tuning thresholds for Canny Edge Detection to optimize results.
- Filtering noise while preserving meaningful object details.

### **Learnings:**
- **Python** offers high flexibility and scalability for custom workflows.
- **MATLAB** simplifies implementation with robust built-in functions.
- Proper preprocessing (grayscale conversion, noise removal) significantly improves results.

---

## Conclusion and Future Work

### **Conclusion:**
- The project successfully implemented and compared **edge detection** and **object segmentation** using **Python** and **MATLAB**.
- **Python** provided flexibility for customizations, while **MATLAB** offered efficient built-in functions for rapid prototyping.
- Metrics validated the accuracy and efficiency of both implementations.

### **Future Work:**
- Extend the methodology to handle **colored images** and **video streams**.
- Explore **deep learning-based segmentation techniques**, such as **Mask R-CNN**.
- Optimize implementations for **real-time applications**.

---


