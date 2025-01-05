# Frequency Matching Tool using Python

## Project Title
**Frequency Matching Tool with Spectrogram-Based Image Retrieval**

## Team Member
- Swetha Kuruva
- Shashidhar Reddy Virupa

---

## Project Overview
This project implements a **Frequency Matching Tool** with a **Graphical User Interface (GUI)** using Python. The primary objective is to analyze and retrieve images from a dataset based on their frequency spectrograms, enabling efficient and intuitive frequency-based image comparison. The system features a user-friendly GUI that allows users to query images, compute their spectrograms, and retrieve visually similar images from the dataset. The frequency analysis is performed using the **2D Short-Time Fourier Transform (STFT)**.

---

## Features
- **Dataset Loader**: Load and preprocess a dataset of images for frequency analysis.
- **Query Selection**: Users can select a query image from their local storage.
- **Frequency-Based Image Matching**: Computes spectrograms and retrieves the top matching images based on frequency similarity.
- **Spectrogram Visualization**: Displays the spectrograms of the query and matched images.
- **Result Display**: Shows correlation scores alongside the top matches in the GUI.
- **Clear Interface Option**: Resets the GUI to its initial state for a new query.
- **Interactive GUI**: Simple and intuitive interface for smooth user interaction.

---

## Dataset
The dataset used for this project is the **Kaggle Natural Images Dataset**, which contains diverse image categories, including airplanes, flowers, fruits, and animals.

- **Source**: [Kaggle - Natural Images Dataset](https://www.kaggle.com/prasunroy/natural-images)
- **Dataset Size**: Approximately 150 MB
- **Contents**: 6,899 images categorized into multiple folders based on object types.
- **Preprocessing**: Images were resized to `256x256` pixels and converted to grayscale for accurate spectrogram computation.

---

## Requirements
- **Python Environment**: Python 3.8 or higher
- **Libraries**: OpenCV, NumPy, Matplotlib, Tkinter, Pillow, Scipy
- **System Requirements**: Compatible with Windows, macOS, and Linux

---

## Installation and Usage

### Clone this repository to your local machine:
```bash
git clone https://github.com/swethakuruva/Frequency-Matching-Tool.git

## Install the required Python libraries:
- pip install -r requirements.txt

## Run the main script to launch the GUI:
- python frequency_matching_gui.py

Use the GUI to:
1. Load the dataset folder.
2. Select a query image from your system.
3. View spectrograms and retrieve top matching images based on frequency similarity.
4. Clear the results for a new query.

## Code Overview

This project contains the following main files:

1. **frequency_matching_gui.py**
   - This file contains the main GUI code for the project. It includes functionalities to load the dataset, select a query image, compute spectrograms, and display the results in a user-friendly interface.

2. **spectrogram_computation.py**
   - This script is responsible for calculating the 2D Short-Time Fourier Transform (STFT) for frequency analysis. It generates spectrograms and calculates similarity metrics for image comparison.

3. **batch_processing.py**
   - Automates the processing of the entire dataset to compute and store spectrograms for faster retrieval and comparison.

4. **image_retrieval_utils.py**
   - Provides helper functions for preprocessing images, computing frequency correlations, and handling datasets efficiently.

# Output

The tool produces the following outputs:

1. **Query Image and Spectrogram**: Displays the selected image and its spectrogram.
2. **Top Matches**: Shows the top matching images and their respective spectrograms, ranked by similarity.
3. **Correlation Scores**: Numerical values indicating the similarity between the query and matched images.

---

## Example Outputs

**Query Image and Spectrogram**

**Top Matches**

| Match   | Similarity Score |
|---------|------------------|
| Match 1 | 0.89             |
| Match 2 | 0.85             |
| Match 3 | 0.83             |

---

## Challenges Faced

1. **Dataset Preprocessing**: Converting images to grayscale and resizing them consistently required computational effort.
2. **Spectrogram Computation**: Optimizing the STFT process for large datasets was a significant challenge.
3. **GUI Design**: Integrating real-time processing with a responsive and user-friendly GUI required careful implementation.
4. **Error Handling**: Ensuring the tool could handle corrupted or missing files in the dataset without crashing.

---

## Conclusion

The **Frequency Matching Tool** successfully demonstrates the use of spectrograms for frequency-based image analysis and retrieval. By combining computational techniques with an intuitive GUI, this tool simplifies complex image comparison tasks, making it accessible for diverse applications in pattern recognition, content analysis, and digital asset management.

---

## Acknowledgments

- **Kaggle Natural Images Dataset**: The primary dataset used for this project.
- **Open-source Python libraries**: OpenCV, NumPy, Matplotlib, and more for facilitating image analysis and GUI development.
