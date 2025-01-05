import streamlit as st
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt

def color_transfer(source, target):
    
    # converting the source and target images into array and RGB format.
    src_file = np.array(source.convert('RGB'))
    tar_file = np.array(target.convert('RGB'))

    # Converting the source and target array into LAB channel format.
    src_lab_channel = cv2.cvtColor(src_file, cv2.COLOR_RGB2LAB)
    src_lab_channel = src_lab_channel.astype(np.float32)


    tar_lab_channel = cv2.cvtColor(tar_file, cv2.COLOR_RGB2LAB)
    tar_lab_channel = tar_lab_channel.astype(np.float32)

    # Computing the mean and std for each LAB channel.
    # src_mean and src_std consists of the mean and std value of each LAB channel from the source image.
    # tar_mean and tar_std consists of the mean and std value of each LAB channnel from the target image.
    src_m, src_std = cv2.meanStdDev(src_lab_channel)
    tar_m, tar_std = cv2.meanStdDev(tar_lab_channel)

    # LAB color channels are represented as, L-Lightness, A-Green and Red, B-Blue and Yellow.
    # Lab color channels are splitted individually from the target image.
    l_light, a_green, b_blue = cv2.split(tar_lab_channel)

    # Normalising the LAB Channels of the target label using mean and std to match with the source image label.
    l1_mean = l_light - tar_m[0][0]
    l1_std = (src_std[0][0] / tar_std[0][0])
    l_norm = (l1_mean * l1_std) + src_m[0][0]

    a1_mean = a_green - tar_m[1][0]
    a1_std = (src_std[1][0] / tar_std[1][0])
    a_norm = (a1_mean * a1_std) + src_m[1][0]

    b1_mean = b_blue - tar_m[2][0]
    b1_std = (src_std[2][0] / tar_std[2][0])
    b_norm = (b1_mean * b1_std) + src_m[2][0]

    # Clipping the normalised LAB labels in the range between [0 - 255], since the image pixel range is from [0 - 255].
    clip_l = np.clip(l_norm, 0, 255)
    clip_a = np.clip(a_norm, 0, 255)
    clip_b = np.clip(b_norm, 0, 255)

    # Merging the LAB Channels back into a single LAB Image and converting back into RGB format.
    result_lab = cv2.merge([clip_l, clip_a, clip_b])
    result_rgb = cv2.cvtColor(result_lab.astype(np.uint8), cv2.COLOR_LAB2RGB)

    return result_rgb

# Title for our Streamlit application.
st.title("Color Transfer using LAB Channels.")

# creating a file_uploader widget which navigates the user to choose the approriate image type.
source_image_file = st.file_uploader("Please Choose the Source Image. . .", type=["jpg", "jpeg"])

# Chec if the file is uploaded correct or not.
if source_image_file is not None:
    # Open the image file using PIL "open" function.
    source_img_file = Image.open(source_image_file)

    # Displaying the uploaed image using streamlit image function.
    st.image(source_img_file, caption='Source Image.', use_container_width=True)
    # This will help us to write a caption, once the image is successfully uploaded.
    st.write("Source Image Succesfully Uploaded . . .")
else:
    # If the image is not uploaded, it will prompt us to upload the image.
    st.write("Please upload the source image file . . .")

# Choosing the target image file.
target_image_file = st.file_uploader("Please Choose the Target Image . . .", type=["jpg", "jpeg"])

if target_image_file is not None:
    # Open the image file using PIL
    target_img_file = Image.open(target_image_file)

    # Display the uploaded target image.
    st.image(target_img_file, caption='Target Image.', use_container_width=True)
    st.write("Target Image successfully uploaded . . .")
else:
    st.write("Please upload the target image file . . .")


# st.button will call the color_transfer(), which will give us the final resulting image.
if st.button('Transfer Colors'):
    if source_image_file is not None and target_image_file is not None:
        # calling color_transfer() by passing in source and target image files.
        result_image = color_transfer(source_img_file, target_img_file)
        # Converting the Numpy array to actual image using PIL functions.
        result_image_pil = Image.fromarray(result_image)
        # Finally, below line will display the resulting color transfered image.
        st.image(result_image_pil, caption='Color Transferred Image.', use_container_width=True)
    else:
        # Display message, if no image files were uploaded.
        st.write("Please upload both source and target images.")






