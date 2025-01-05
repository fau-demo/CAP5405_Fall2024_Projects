# **Mosaic-Image-Generator**

Mosaic Generator is a Python-based tool that creates stunning photo mosaics using an input image and a dataset of tile images.

## **Team Members**
**Kurady Rathnasree Kalkura**

## **Software Used**
This project utilizes the following software and libraries:
- **Python 3.10+**
- **Libraries:**
  - `Pillow`: For image processing (loading, resizing, and saving images).
  - `NumPy`: For efficient mathematical operations (e.g., calculating averages and histograms).
  - `Tkinter`: For creating the graphical user interface (GUI).
  - `JSON`: For caching tile information (average color and histograms) to optimize performance.

## **Project Description**
The Mosaic Generator converts an input image into a photo mosaic by dividing it into smaller blocks and replacing each block with the best-matching image from a dataset of tile images.

### **Key Features**
- **Matching Algorithms**:
  1. **Average Color Matching**: Matches tiles based on the average color of the image block.
  2. **Histogram Matching**: Matches tiles based on color histograms, ensuring more detailed texture matching.
- **Tile Reuse Control**: Ensures tiles are not reused unless necessary, improving the aesthetic appeal.
- **Caching for Performance**: Saves computed tile data (average colors and histograms) in a cache file (`tile_cache.json`) to optimize future mosaic generation.
- **User-Friendly GUI**: Easy-to-use graphical interface to select input images, datasets, tile size, and matching algorithm.

### **Advantages**
- Avoids repetitive computation by using a caching mechanism.
- Supports both color and texture-based matching for more flexibility.
- Provides an interactive GUI for seamless operation.

## **Installation and Usage**

### **Installation Steps**
1. **Clone the Repository**:
   Clone the GitHub repository to your local machine:
   ```bash
   git clone https://github.com/your-username/Mosaic-Generator.git
   cd Mosaic-Generator
   ```

2. **Install Dependencies**:
   Use `pip` to install the required Python libraries:
   ```bash
   pip install pillow numpy
   ```

3. **Prepare Your Dataset**:
   - Place your dataset of tile images in a folder (e.g., `tiles_dataset/`).
   - Ensure all images are in `.jpg`, `.jpeg`, or `.png` format.

4. **Run the Program**:
   Launch the GUI tool by executing:
   ```bash
   python mosaic_gui.py
   ```

### **Using the GUI**
1. **Input Image**: Select the main image you want to convert into a mosaic.
2. **Dataset Folder**: Choose the folder containing the tile images.
3. **Tile Size**: Enter the desired size of the tiles (e.g., 5 0r 10 pixels).
4. **Matching Algorithm**: Select one of the following:
   - **Average Color Matching**: Matches based on the average color of each block.
   - **Histogram Matching**: Matches based on histogram comparison for better texture matching.
5. **Generate Mosaic**: Click the "Generate Mosaic" button to create the mosaic and save it as `mosaic_output.jpg`.

### **Expected Output**
- The generated photo mosaic is saved as `mosaic_output.jpg` in the project directory.
- A preview of the mosaic is displayed in the GUI.

## **Input Image Requirements**
- **Supported Formats**: `.jpg`, `.jpeg`, `.png`, `.bmp`
- **Recommended Resolution**: At least **500x500 pixels** for better results.
- **Aspect Ratio**: The tool maintains the aspect ratio of the input image while dividing it into uniformly sized tiles.

## **Operating System Compatibility**
- Tested on **Windows** (may work on other systems if dependencies are installed).

## **Project Workflow**
1. **Tile Preprocessing**: 
   - Each tile is resized to the specified size.
   - Average color and histograms are calculated and stored in the cache.
2. **Mosaic Generation**:
   - The input image is divided into blocks.
   - Each block is matched to the most suitable tile based on the selected algorithm.
3. **Caching for Optimization**:
   - Cached tile data reduces computation time for subsequent mosaic generations.

## **Performance Tips**
- Use high-quality tile images for better mosaic results.
- Larger datasets improve matching accuracy.
- Adjust tile size to balance between output quality and performance.

## **References and Resources**
- **Python Documentation**:
  - [Pillow Documentation](https://pillow.readthedocs.io/en/stable/)
  - [NumPy Documentation](https://numpy.org/doc/)
- **Community Help**:
  - [Stack Overflow](https://stackoverflow.com/) for debugging and troubleshooting.
- [GeeksforGeeks Python Tutorials](https://www.geeksforgeeks.org/python-tkinter-tutorial/)
