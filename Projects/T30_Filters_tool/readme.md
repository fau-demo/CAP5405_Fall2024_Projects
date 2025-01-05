# TITLE OF THE PROJECT :Instagram-Like Filters Tool
PROJECT TEAM MEMEBERS  : M.Ram Nagendra Kumar

# Software Used
- **Python 3.6+**: Core programming language for developing the application.  
- **Tkinter**: Used for building the graphical user interface (GUI).  
- **Pillow (PIL)**: Used for image loading, manipulation, and saving.  
- **JSON**: Used for storing and managing filter configurations.  


This project is a Python-based GUI application that applies Instagram-style filters to images. Built with `Tkinter` for the GUI and `Pillow` for image manipulation, this application allows users to load an image, preview filters in a grid layout, apply filters dynamically, and save the edited image. Users can adjust filter settings with sliders and checkboxes, making the application highly customizable.

## Features

- **Image Loading**: Load any JPG or PNG image into the app.
- **Filter Previews**: Display a grid of Instagram-style filter previews with names and thumbnails.
- **Adjustable Filters**: Modify brightness, contrast, saturation, and grayscale for each filter.
- **Dynamic Application**: Automatically apply filter changes as slider values are adjusted.
- **Save Edited Image**: Save the filtered image to a file.

## Filters Available

The filters are loaded from a JSON file, each with specific settings:
- `Brightness`
- `Contrast`
- `Saturation`
- `Grayscale`

Some sample filters include "Bright," "Cool," "Warm," "Grayscale," and others.

## Input Image Requirements  
- **Supported Formats**: JPG, PNG.  
- **Recommended Size**: Images should ideally be under 5MB to ensure smooth performance.  

## Supported Operating Systems  
- **Windows**  
- **Linux**  

## References and Resources  
- **Pillow Documentation**: [https://pillow.readthedocs.io](https://pillow.readthedocs.io)  
- **Tkinter Documentation**: [https://docs.python.org/3/library/tkinter.html](https://docs.python.org/3/library/tkinter.html)  


## Project Structure

```plaintext
Instagram-Like-Filters-Tool/
├── filterpreviews/                # Folder for filter preview images (e.g., bright.jpg, cool.jpg)
├── filters.json                    # JSON file with filter configurations
├── main.py                         # Main Python script for running the application
├── requirements.txt                # List of dependencies
└── README.md                       # Project documentation
```
## Getting Started

### Prerequisites

Ensure you have Python 3.6 or later installed on your system.

### Setup Instructions

1. **Clone the repository**:

```bash
   git clone https://github.com/RAM6571/Instagram-Like-Filters-Tool.git
   cd Instagram-Like-Filters-Tool
 ```

2. **Install Dependencies:**:

Install all required Python libraries using requirements.txt:

```bash
    pip install -r requirements.txt
```


3. **Run the Application:**:

Install all required Python libraries using requirements.txt:

```bash
    python main.py
```

