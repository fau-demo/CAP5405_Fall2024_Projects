# Color-Based-Image-Retrieval-using-MATLAB
## Project Title
Color-Based Image Retrieval System (CBIRS)


## Team Member
- **Naga Prem Sai Nellure**


## Project Overview
This project implements a **Color-Based Image Retrieval System (CBIRS)** using MATLAB. The primary goal is to retrieve images from a dataset based on their color composition, enabling efficient digital asset management. The system employs a Graphical User Interface (GUI) for ease of use, allowing users to query images by selecting a reference image. The retrieval process is based on RGB histogram matching.


## Features
- **Dataset Loader:** Load a dataset of images for analysis.
- **Query Selection:** Users can select a query image to retrieve similar images based on color similarity.
- **Image Matching:** Displays the top five matches for the query image alongside their RGB histograms.
- **Clear Option:** Allows users to reset the interface.
- **RGB Histogram Comparison**: Used for image similarity measurements.
- **Simple GUI**: User-friendly interface for intuitive interaction.


## Dataset
The dataset used in this project is the **Oxford 102 Flower Dataset**, which contains 102 flower categories.
- **Source:** [Kaggle - Oxford 102 Flower Dataset](https://www.kaggle.com/datasets/nunenuh/pytorch-challange-flower-dataset)
- **Dataset Size:** Approximately 330 MB.
- **Contents:** 8,189 images across 207 folders with diverse floral compositions.


## Requirements
- **MATLAB**: Version 2021b or higher, including MATLAB App Designer for GUI development.
- **Toolboxes**: Image Processing Toolbox.
- **Operating System**: Compatible with Windows, Linux, and macOS.


## Installation and Usage
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/Premsai8991/Color-Based-Image-Retrieval-using-MATLAB.git
2. Open MATLAB and navigate to the folder containing the project files.
3. Run the script colorImageRetrievalGUIClear.m to launch the GUI.
4. Follow these steps in the GUI:
   - Load Dataset: Click to load the dataset folder containing the images.
   - Select Query Image: Choose a query image from your computer to find matches.
   - View Results: Observe the top five matching images and their respective RGB histograms.
   - Clear Images: Reset the GUI to its default state.


## Format and Size of Input Images
- The system processes images in .jpg format.
- Images are resized to 224x224 pixels for consistent histogram calculations.


## Code Overview
This project contains the following main files:
1. **[`colorImageRetrievalGUIClear.m`](https://github.com/Premsai8991/Color-Based-Image-Retrieval-using-MATLAB/blob/main/colorImageRetrievalGUIClear.m)**  
   - This file contains the main GUI code for the project. It includes functionalities to load the dataset, select a query image, compute histograms, and display the results in a user-friendly interface.
2. **[`loadDataset.m`](https://github.com/Premsai8991/Color-Based-Image-Retrieval-using-MATLAB/blob/main/loadDataset.m)**  
   - This script is responsible for loading and preprocessing the image dataset, calculating histograms, and storing them for comparison.
3. **[`TestRGBModel.m`](https://github.com/Premsai8991/Color-Based-Image-Retrieval-using-MATLAB/blob/main/TestRGBModel.m)**  
   - This file includes RGB model tests for comparing images using average RGB values.
4. **[`imageLabels.m`](https://github.com/Premsai8991/Color-Based-Image-Retrieval-using-MATLAB/blob/main/imageLabels.m)**  
   - Provides helper functionality for labeling and organizing images in the dataset.


## Output
The GUI displays:
1. Query Image: The selected image by the user.
2. Top 5 Matches: Images most similar to the query image based on RGB histogram comparison.
3. RGB Histograms: Visual representation of the color composition for the query and matched images.


## Example Outputs
Below are some example outputs of the GUI after executing the project:

#### GUI Window 
![CBIRS Output 1](CBIRS%20Output%201.png)

#### Clear Window State
![Clear Window Output](CBIRS%20Output%201%20Clear%20window.png)

#### Query and Matches Display
![CBIR Output 2](CBIR%20Output%202.png)
![CBIR Output 3](CBIR%20Output%203.png)
![CBIR Output 4](CBIR%20Output%204.png)
![CBIR Output 5](CBIR%20Output%205.png)


## Acknowledgments
- The dataset was sourced from the Kaggle repository.
- Project guidance provided by Dr. Velibor Adzic.
