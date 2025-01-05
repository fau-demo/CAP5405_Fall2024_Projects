# Colour-Transfer
# Color Palette Transfer Tool

## Team Members

1.  Praneeth Kumar Reddy Pappu - Z23747763
2.  Devi Sree Repani - Z23809939

## Overview

The Color Palette Transfer Tool is a GUI-based application built with
Python that allows users to transfer color palettes between images. The
tool uses the LAB color space for precise color adjustments, ensuring
natural and visually pleasing results. With an intuitive user interface,
the tool is accessible to both novice and experienced users.

## Features

-   Base Image Selection: Choose the base image whose color palette will
    be applied.\
-   Target Image Selection: Select the target image where the colors
    will be transferred.\
-   Real-Time Preview: View the processed image directly in the
    application.\
-   Image Saving: Save the result as a new file for further use.

## Software Stack

-   Python: Core programming language.\
-   tkinter: For creating the graphical user interface.\
-   OpenCV: For image processing and manipulation.\
-   Pillow: For handling image display in the GUI.

## Operating System

-   The program runs on Windows and Linux with python installed.

## How to get gui

1)  Run the file gray_gui.py from command line with the command python
    gray_gui.py.
2)  GUI will be loaded.
3)  Use the gui to do the processing.

## Input Image Requirements:

-   Format: Supported formats are .jpg, .png, .jpeg, and .bmp.
-   Size: Images of any size are supported, but they will be resized for
    display in the GUI.

## How GUI Works

1.  Image Upload: Users upload a base image and a target image.\
2.  Color Space Conversion: Images are converted to the LAB color space,
    which separates brightness (L) from color components (A and B).\
3.  Statistical Adjustment: The mean and standard deviation of the LAB
    channels in the base image are used to adjust the target image's LAB
    channels.\
4.  Transformation and Display: The adjusted target image is converted
    back to RGB and displayed in the GUI.\
5.  Saving: The processed image can be saved locally.

## References

-   OpenCV documentation: https://docs.opencv.org/
-   Pillow (PIL Fork): https://pillow.readthedocs.io/
-   tkinter Python documentation:
    https://docs.python.org/3/library/tkinter.html
