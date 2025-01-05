**JPEG Compression and Decompression**

**TITLE**

Simple JPEG codec

Implement a simple version of JPEG encoder and decoder.

**Project description:**

This project implements a simplified JPEG codec for compressing and decompressing images, focusing on the core steps of JPEG compression, including Discrete Cosine Transform (DCT), quantization, zigzag scanning, Huffman coding, and Inverse DCT (IDCT). The codec efficiently reduces the file size during encoding and reconstructs the image during decoding, retaining a high degree of visual quality.
Below is the output which we got for example image which we took i.e., Lenna test image which is widely used standard test image in the field of image processing,it is a cropped 512x512 pixel.
![C19BF5AB-AE8D-4BC9-946A-D14761AC728B_1_105_c](https://github.com/user-attachments/assets/a0b9863e-89b3-4f7e-92e3-8165f4454903)

**TEAM MEMBERS**

Bhavana Shree Akulapally 

Sai Dheeraj Reddy LNU 

Karthik Reddy Manukonda 

Laya Yellanki 



**Features:**

Compression: 
Encodes grayscale images using DCT, quantization, zigzag scanning and Huffman coding.

Decompression:
Reconstructs images from the compressed data preserving quality.

Performance Metrics: 
Calculates Peak Signal-to-Noise Ratio (PSNR) to evaluate the quality of the reconstructed image.

Visualization: 
Displays original and reconstructed images along with a visualization of the compressed image (quantized coefficients).


**Project Structure**

encode_image(image): Encodes the image using JPEG compression techniques.

decode_image(encoded_data, huffman_tree, shape): Decodes the compressed image back to its original format.

psnr(original, reconstructed): Computes the PSNR value to measure reconstruction quality.


**Utility functions:**

load_image(filepath): Loads an image and converts it to grayscale.

save_image(filepath, image): Saves the image to a file.

display_images(original, reconstructed): Displays the original and reconstructed images side by side.

visualize_compressed_image(encoded_data, huffman_tree, shape): Visualizes the compressed image using quantized coefficients.


**Requirements**

This project requires the following Python libraries:

numpy

Pillow

matplotlib

scipy

You can install the dependencies using:

pip install numpy pillow matplotlib scipy

**Usage:**

Clone the repository or download the project files.

Replace the image_path variable in the script with the path to your grayscale image.

Run the script to:

Compress the image and save the compressed data to a binary file.

Decompress the binary file and reconstruct the original image.

Evaluate the quality of the reconstructed image using PSNR.

Save the reconstructed image and visualize the compressed image.

**Results**

Displays the original and reconstructed images for comparison.

Prints the PSNR value to indicate the quality of reconstruction.

Saves the reconstructed image as reconstructed_image.jpg.


**Limitations**

This implementation supports only grayscale images.

The Huffman encoding process may have limited scalability for very large datasets.

**Input Format for the Simplified JPEG Codec**

**Supported Image Types:**

The codec will primarily support grayscale images (single-channel) in standard image formats such as:
.jpg, .jpeg,
.png,
.bmp,
.tiff

**Compatibility**:

Windows

macOS

Linux

**Flowchart Representation:**

Input Image → Preprocessing → Grayscale Conversion → 8x8 Blocks

Blocks → DCT → Quantization → Zigzag Scanning → Huffman Encoding → Compressed Data(save to binary file)

Compressed Data → Huffman Decoding → Reverse Zigzag → Dequantization → IDCT → Reconstructed Image

This structure provides a clear pipeline for encoding and decoding operations in the simplified JPEG codec.

**REFERENCES**:

1.JPEG Compression Fundamentals:

Gonzalez, R. C., & Woods, R. E. Digital Image Processing. Pearson.

2.Python Libraries for Image Processing:

NumPy Documentation: https://numpy.org/doc/

Pillow (Python Image Library) Documentation: https://pillow.readthedocs.io/

3.Discrete Cosine Transform (DCT):

Simplified explanations: https://en.wikipedia.org/wiki/Discrete_cosine_transform

4.Huffman Coding:

tutorial: https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/

5.Zigzag Scanning:

JPEG zigzag order concept: https://en.wikipedia.org/wiki/JPEG#Entropy_coding






