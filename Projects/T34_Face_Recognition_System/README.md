Face Recognition Using Classical Image Processing
Project Title
Face Recognition Using Classical Image Processing Techniques (FRUCIPT)

Team Member
harsha
Project Overview
This project implements a Face Recognition System using Classical Image Processing Techniques. The primary goal is to identify and recognize faces in a dataset based on their pixel-level similarities, enabling lightweight and interpretable recognition without relying on machine learning models. The system uses Euclidean distance for comparison and generates confidence scores to rank matches. Visual tools such as heatmaps and RGB histograms further aid in understanding the results.

Features
Dataset Loader: Load and preprocess the face dataset for analysis.
Query Image Selection: Select a query image to find the closest matches from the dataset.
Image Matching: Retrieve the top three matches for the query image using Euclidean distance.
Heatmap Visualization: Highlight pixel-level differences between the query and matched images.
Confidence Scoring: Generate confidence levels based on similarity scores.
RGB Histogram Analysis: Display RGB histograms for the query and matched images.
Lightweight Implementation: A purely classical approach for face recognition with no dependency on machine learning.
Dataset
The dataset used in this project is the Labeled Faces in the Wild (LFW) dataset, a standard benchmark for face recognition.

Source: LFW Dataset Official Page
Dataset Size: Approximately 233 MB.
Contents: 7,967 images of faces, each labeled with the person’s name.
Subset for Testing: A random selection of 10 images was used for matching experiments to ensure efficiency in testing and validation.
Requirements
Programming Language: Python 3.7 or higher.
Libraries:
numpy: For numerical computations.
opencv: For image processing tasks.
matplotlib: For data visualization.
Operating System: Compatible with Windows, Linux, and macOS.
Installation and Usage
Clone this repository to your local machine:
bash
Copy code
git clone https://github.com/your_username/Face-Recognition-Classical.git
Ensure all required libraries are installed:
bash
Copy code
pip install numpy opencv-python matplotlib
Download and extract the LFW dataset into your project directory.
Run the script faceRecognition.py to execute the project.
Follow these steps during execution:
Load Dataset: Preprocess the dataset to resize, normalize, and flatten images.
Select Query Image: Choose a test image for recognition.
View Results: Observe the top three matches along with heatmaps and RGB histograms.
Confidence Scores: Validate matches with numerical confidence levels.
Format and Size of Input Images
Input images are expected in .jpg or .jpeg format.
Images are resized to 100x100 pixels for consistency in calculations.
Code Overview
This project contains the following main files:

faceRecognition.py

The main script that loads the dataset, preprocesses images, and performs face recognition.
Implements Euclidean distance for similarity scoring and heatmap generation.
preprocess.py

A utility module for converting images to grayscale, resizing, and normalizing pixel intensities.
visualization.py

Contains functions for generating heatmaps and plotting RGB histograms for visual comparison.
Output
The system outputs the following:
![image](https://github.com/user-attachments/assets/2d24b41f-218d-4d09-82c4-9215cf8756cf)

Test Image: The input image selected by the user.
Top Matches: The top three images in the dataset that are most similar to the test image.
Difference Heatmaps: Pixel-level differences between the test image and matches.
RGB Histograms: Color composition analysis of the test image and matches.
Confidence Scores: Numerical scores indicating the reliability of matches.
Example Outputs
Example 1
Recognition Result:



Test Image: Aaron Eckhart
Top Match: Bridget Fonda
Confidence Score: 35.15%
Heatmap & Histogram:
Example 2
Recognition Result:

Test Image: Aaron Eckhart
Top Match: Donald Rumsfeld
Confidence Score: 34.44%
Heatmap & Histogram:
Example 3
Recognition Result:

Test Image: Aaron Eckhart
Top Match: Gerhard Schroeder
Confidence Score: 34.15%
Heatmap & Histogram:
Acknowledgments
The LFW dataset was sourced from its official website, a widely recognized benchmark for face recognition research.
Special thanks to the open-source community for developing and maintaining libraries like OpenCV and Matplotlib, which are critical to this project.
