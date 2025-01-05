
## Project title: Color-Based Image Retrieval System  

## Team members
- Jayanth Reddy PIDUGU - Z23749471
- Sri Sunith Raju TATAPUDI - Z23750460



A Python-based application for retrieving images from a dataset based on user-selected colors. This project allows users to select a color using a color picker or by entering a HEX code. The system processes images, extracts their dominant colors using KMeans clustering, and matches images that are visually similar to the selected color.

---

## Features  
- **Dominant Color Extraction**: Uses KMeans clustering to determine the top 5 dominant colors in each image.  
- **Custom Color Matching**: Allows users to search for images by selecting a color using a color picker or entering a HEX code.  
- **Dynamic Thresholding**: Matches images based on the Euclidean distance between colors.  
- **GUI Interface**: Provides a user-friendly interface using Tkinter.  
- **Result Saving**: Saves matching images to a designated output folder.  

---
## Operating Systems supported
- Windows
- MacOS
- Linux

## Software Used
- Python 3.7 or later
- Tkinter
- scikit-learn
- Pillow
- numpy

## Prerequisites  

Make sure you have the following installed on your system:  
- Python 3.7 or later  
- Required Python libraries:  
  ```bash
  pip install numpy pillow scikit-learn
  ```  

---

## Dataset Structure  

Place your dataset images in a folder named `image_data` located in the same directory as the script. Supported formats are `.jpg` and `.png`.  

Example structure:  
```plaintext
project-folder/
│
├── image_data/
│   ├── image1.jpg
│   ├── image2.png
│   └── ...  
├── matched_images/ (Generated after searching)
├── image_data.json (Generated after processing)
├── color_retrieval.py
└── README.md  
```

---

## How to Run  

1. **Process the Dataset**  
   - Click the **Process Dataset** button in the GUI to extract dominant colors from all images.  
   - This will generate a `image_data.json` file containing image names and their dominant colors.  

2. **Search Images by Color**  
   - Click the **Search Images by Color** button in the GUI.  
   - Choose a color using the color picker or enter a HEX code to find matching images.  
   - All matched images will be copied to the `matched_images` folder.  

3. **Quit Application**  
   - Click the **Quit** button to exit the application.  

---

## Project Structure  

### Main Functions  
- `process_dataset()`: Processes the images in the dataset folder and extracts their dominant colors using KMeans clustering.  
- `load_dataset()`: Loads the `image_data.json` file containing the processed image data.  
- `hex_to_rgb(hex_color)`: Converts a HEX color code to RGB format.  
- `match_images(user_color)`: Matches images from the dataset with colors close to the user-provided color.  
- `search_images()`: Opens a dialog for color selection, matches images, and saves the results to the output folder.  

### GUI Components  
- **Tkinter** is used for creating a simple and intuitive graphical user interface:  
  - `Process Dataset` Button  
  - `Search Images by Color` Button  
  - `Quit` Button  

---

## How the Matching Works  
1. Extracts the top 5 dominant colors from each image using KMeans clustering.  
2. Compares the user-selected color with these dominant colors using Euclidean distance.  
3. Matches images with a distance below a specified threshold (default: 50).  

---

## Example Output  

After a successful search, matched images are saved to the `matched_images` folder:  
```plaintext
matched_images/
├── matched_image1.jpg
├── matched_image2.png
└── ...  
```  

---

## References
- KMeans clustering algorithm from scikit-learn.  https://scikit-learn.org/stable/index.html
- Euclidean distance formula for color comparison
- Tkinter documentation for creating the GUI . https://docs.python.org/3/library/tkinter.html

## Future Enhancements  
- Add support for additional image formats.  
- Allow users to adjust the matching threshold dynamically.  
- Enable batch processing for large datasets.  


