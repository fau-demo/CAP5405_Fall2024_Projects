# Al the necessary libraries to be installed 
import streamlit as st
import numpy as np
from skimage import io, color, filters
from skimage.morphology import binary_erosion as bwerode, erosion as erode
from skimage.morphology import skeletonize
from scipy.spatial.distance import directed_hausdorff
import skimage.morphology as mo
import scipy.ndimage as ndi
import skimage.transform as transform
import pandas as pd
import math

#Using streamlit the ui was divide into columns separately for uploading base image and images to be compared.
col1, col2 = st.columns(2)
file_list = []#Using the file list to add all the images and get a count of them to be dispalyed in rows of 4 columns

#The first column as mentioned above uses the file_uploader functionality of streamlit ot upload a base image of type jpg, jpeg, or png.
#More image types can be added on a need basis
with col1:
    st.caption("Upload base image:")
    st.markdown("---")
    baseImage = st.file_uploader("Upload the base image:", type=["jpg", "jpeg", "png"])
    if baseImage is not None:
        cola, colb, colc = st.columns(3)
        with cola:
            st.image(baseImage)

#The images to compared are split into rows of 4 each and the same type of images similar to base image are included. More types can be included on need basis.
with col2:
    st.caption("Upload one or more images to be compared with:")
    st.markdown("---")
    images = st.file_uploader("Upload one or more images:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if images is not None:
        for img in images:
            file_list.append(img)
        rows = math.ceil(len(file_list)/4)
        col1,col2,col3,col4=st.columns(4)
        
        for i in range(rows):
            with col1:
                if(i*4 + 0) < len(file_list):
                    st.image(file_list[i*4 + 0])
            with col2:
                if(i*4 + 1) < len(file_list):
                    st.image(file_list[i*4 + 1])
            with col3:
                if(i*4 +2) < len(file_list):
                    st.image(file_list[i*4 + 2])
            with col4:
                if(i*4 + 3) < len(file_list):
                    st.image(file_list[i*4 + 3])

#button has been added to the similarity function only when clicked.
button_clicked = st.button("Compare")

#Logic for converting a color iamge to grayscale using scikit library
def toGrayScale(image):
# Convert to grayscale if necessary
    if image.ndim == 3:
        gray_image = color.rgb2gray(image)
        return gray_image
    
#Similaryly code for converting grayscale to binary using threshold before convering to binary
def toBinary(image):
    threshold = filters.threshold_otsu(image)
    binary_image = image > threshold
    return binary_image



# structuring element ir kernel. Here 5 by 5 has been used, 3 by 3 can be used as well.
kernel = np.ones((5, 5), np.uint8)

#Created a dataframe using pandas to display the similarity results in a tabular fashion
df = pd.DataFrame(columns=['Image Name', 'Similarity using Jaccard Index'])

#When the compare button is clicked, first the logic checks if the base image is empty or not
#prompting the user to upload image, and if images is empty, it displays an empty table of results
if(button_clicked):
    if ((baseImage is not None) and (images is not None)):
        #All the necesary images are first converted to grayscale and then binary. THen erode/skeletonize are
        #used for their invidual logics instead of bwerode.
        base_img = io.imread(baseImage, 0)
        baseImage_grayscale = toGrayScale(base_img)
        baseImage_binary = toBinary(baseImage_grayscale)
        baseImage_skeleton = skeletonize(baseImage_binary) #Comment this out for erode comparison and uncomment for skeleton comparison
        #baseImage_eroded = erode(baseImage_binary, kernel)#Comment this out for skeleton comparison and uncomment for erode comparison

        #iterate through each image and compare it with base image and add the similarity result rowwise using jacquard index to the dataframe
        for img in images:
            imageName = img.name
            img = io.imread(img, 0)
            img_grayscale = toGrayScale(img)
            img_binary = toBinary(img_grayscale)
            img_binary_resized = transform.resize(img_binary, baseImage_binary.shape)
            img_skeleton = skeletonize(img_binary_resized)#Comment this out for erode comparison and uncomment for skeleton comparison
            #img_eroded = erode(img_binary_resized, kernel)#Comment this out for skeleton comparison and uncomment for erode comparison


            # Calculate similarity using Jaccard index
            intersection = np.logical_and(baseImage_skeleton, img_skeleton)#Comment this out for erode comparison and uncomment for skeleton comparison
            union = np.logical_or(baseImage_skeleton, img_skeleton)#Comment this out for erode comparison and uncomment for skeleton comparison
            
            #intersection = np.logical_and(baseImage_eroded, img_eroded)#Comment this out for skeleton comparison and uncomment for erode comparison
            #union = np.logical_or(baseImage_eroded, img_eroded)#Comment this out for skeleton comparison and uncomment for erode comparison

            similarity = np.sum(intersection) / np.sum(union)


        
            new_row = {'Image Name': imageName, 'Similarity using Jaccard Index': similarity}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        #Use the dataframe after going through all images to display in a tabular format
        st.dataframe(df)
    else:
        st.caption("Upload required images")#Used when base image is not uploaded

