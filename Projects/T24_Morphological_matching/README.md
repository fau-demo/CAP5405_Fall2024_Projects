# Project-DIP
## Title - Morphological Similarity
This project is about the application of morphological operations to find morphological similarity between images. 
## Team - Asha 
## Project Description:
In this project, a base image is uploaded and one or more images are additionally uploaded to get a score of the morphological similarity between the base image and the other images. A result table is displayed, which gives a good estimate as to which image(s) are closed to the base image. Sci-kit library was used extensively in this project using Python programming language and Streamlit was used for uploading images dynamically and rendering the results on the user interface. The morphological operations employed were eroding and skeletonization. Then Jacquard index was used to compare the similarities between these eroded/skeleton images. The score is between 0 and 1 in a decimal where 1 represents the best/exact match and the closer the score of 0 represents no match.
Inputs, were mostly the color images of horses in different colors, poses and backgrounds. These were first converted to grayscale and then to binary for use in operations. 
Skeletonization was chosen over eroding producing better similarity scores using Jacquard index, basing on visual comparison. In eroding, due to the different images or horses being in different color shades, it chose the ones with the closest color as the most similar rather than the entire object shape.
## Installation and running the project
Project is build using Python for back end coding in conjunction with Streamlit for front end GUI. To run the code the following need to be installed on Windows
- Python
- Visual Studio Code (to run Streamlit seamlessly) instead of Jupyter notebook. 
= Anaconda (easier to install other libraries such as Numpy, Pandas, Scipy etc.) 
- Rest of the libraries can be imported in the code.
## Getting started:
To run the code open a terminal (anaconda prompt) and run the following command
streamlit run main.py
Images of your choice or images from the input folder can be used for this project. Clicking on the compare renders a comparison table for similarity score.
Code has been commented out for eroded images and when similarity is performed using these eroded images.
Comments have been provided the lines to be commented and uncommented for the erode operation to perform similarity and like-wise for skeleton images.
