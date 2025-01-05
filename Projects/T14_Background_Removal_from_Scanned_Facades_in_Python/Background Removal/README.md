The aim of this project is to develop a Python-based solution for removing the background from scanned facades dating from 1924 to 1940 to improve their readability and digital preservation. Many historical documents are scanned in environments where uneven lighting or noise can affect the clarity of the print or the paper upon which they have been drawn is showing signs of decay and mold. By employing digital image processing techniques such as thresholding, edge detection, and morphological operations, we will isolate the textual content from the background. This will help enhance the legibility of faded lines, remove artifacts, and prepare documents for further deep learning applications. The project will utilize libraries like OpenCV and PIL to perform image preprocessing, followed by background subtraction algorithms to create cleaner, more readable document images. Ultimately, this approach aims to automate the restoration of archived architectural drawings, making them more accessible and usable for digital archival purposes. The dataset employed for this project is formatted in 1024x1024 pixel format and features 1784 images of real buildings built in the city of Thessaloniki, Greece designed in the mid-war era.

The proposed project removed the background from the dataset mentioned above using Jupyter Notebook and Python. The libraries imported for this purpose are OS-Lib, cv2, used for image manipulation, matplotlib to check the results of the image transformations as we go and numpy. The final output is saved in .png file format so there is no background for easier further image manipulation or even conversion from pixel to vector format in AutoCAD. 

![image](https://github.com/user-attachments/assets/240efe2c-45af-4d14-8aa5-3ad5297f4969)


Through this methodology, the initial RBG images are first converted into grayscale, a binary mask is created corresponding to the image and lastly the image background is removed and the output saved. 

![image](https://github.com/user-attachments/assets/a8e80bf4-9166-49af-b995-ef96fe49bdc7)


How It Works
 1. Load the Image:
    Read the input images.
 2. Convert to Grayscale:
    Convert the images to grayscale for binary mask creation.

    ![image](https://github.com/user-attachments/assets/e902e85b-8980-4659-a442-b7a9a94d3074)

 4. Create a Binary Mask:
    Uses a threshold to identify the background (white) and foreground (black).

    ![image](https://github.com/user-attachments/assets/e10cf1ef-3e06-4e36-ab2a-298f8025aeb1)

  6. Invert the Mask:
    The background becomes transparent while preserving the foreground.

![image](https://github.com/user-attachments/assets/7a0051ce-1c09-4df4-8ff4-4c02a159f2e4)

  8. Save as Transparent PNG:
    The processed image is saved with a transparent background and black lines.


  10. Visualize the Steps:
    The script displays:
     a. Original Image
     b. Grayscale Image
     c. Binary Mask
     d. Transparent Image with Black Lines

Lastly, the Peak Signal to Noise Ratio is calculated for all images in the dataset to measure whether we have loss of quality during the background removal process. The median PSNR value for all 1784 1024x1024 images is around 33db, indicating good quality retainement during the processing. 
