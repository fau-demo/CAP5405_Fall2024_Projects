# Image Adjustment Tool

---

## Team Members
- Akhil Chatla
- Kavya Vempati

---

## Software Used
1. **Python 3.9 or higher**
2. **PyQt5** - For creating the graphical user interface.
3. **Pillow (PIL)** - For image processing.

---

## Installation Guide

### 1. For Linux Users
#### Step 1: Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/akhil0404-tech/ImageAdjustmentTool.git
cd ImageAdjustmentTool

```

#### Step 2: Install Necessary Linux Packages for PyQt5
Run the following command to install PyQt5 dependencies:
```bash
sudo apt update
sudo apt install python3-pyqt5
```

#### Step 3: Create a Virtual Environment
Navigate to your project directory and create a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 4: Install the Required Python Packages
Install the required packages using `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### 2. For Windows/Mac Users
#### Step 1: Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/akhil0404-tech/ImageAdjustmentTool.git
cd ImageAdjustmentTool

```

#### Step 2: Install PyQt5 and Pillow
Run the following commands to install the necessary Python libraries:
```bash
pip install PyQt5 Pillow
```

#### Step 3: (Optional) Create a Virtual Environment
You can create a virtual environment and install dependencies:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux
pip install -r requirements.txt
```

#### Step 4: Run the GUI Application
You can now run the application:
```bash
python main.py
```

---

## Format and Size of Input Images
1. **Supported Formats**: `.jpg`, `.png`, `.bmp`
2. **Recommended Size**: Images with a resolution of less than 1000 * 800 and smaller than **10MB** for smooth performance.

---

## Project Description
The **Image Adjustment Tool** is an interactive image editing tool inspired by popular applications like Instagram and Snapchat. It enables users to:
1. Adjust image properties such as **brightness**, **contrast**, **saturation**, **exposure**, and **sharpness** using sliders.
2. Apply preset filters like **Sepia**, **Black & White**, **Vintage**, **Cool Tone**, and more.
3. Undo and redo changes for flexible editing.
4. Save the final edited images in various formats.

This tool provides a user-friendly interface using **PyQt5** and processes images efficiently with **Pillow**. It is a perfect application for experimenting with creative effects on photos!
