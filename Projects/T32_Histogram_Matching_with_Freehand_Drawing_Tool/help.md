# Help: Step-by-Step Guide for Using the Histogram Matching Tool

This guide provides detailed steps to help you use the **Histogram Matching with Freehand Drawing Tool** effectively.

---

## Step 1: Launch the Application
1. Open your terminal or command prompt.
2. Navigate to the project directory:
   ```bash
   cd path/to/project
   ```
3. Run the application:
   ```bash
   python main.py
   ```
4. The GUI application will launch.

---

## Step 2: Load Images
1. Click the **"Load Image"** button to select the image you want to process.
2. Click the **"Load Reference Image"** button to select the image whose histogram you want to match.
3. The loaded images will appear in the GUI.

---

## Step 3: Use the Freehand Drawing Tool
1. Use the **"cursor"** to mark areas on the target image that you want to process.
2. You can erase or reset the drawing using the **"Clear Drawing"** button.

---

## Step 4: Apply Histogram Matching
1. Once you’ve marked the desired areas, click the **"Process"** button.
2. The tool will match the histogram of the marked area to the reference image in real time.
3. The processed image will be displayed in the GUI.

---

## Step 5: Export the Processed Image
1. Click the **"Export"** button to save the processed image.
2. Select the destination folder and file format (e.g., JPG, PNG) to save the image.
---

## Supported Input and Output
- **Input Formats**: JPG, PNG
- **Input Image Size**: Recommended dimensions up to 1920x1080.
- **Output Formats**: Same as input format.

---

## Troubleshooting
1. **Application Not Launching**: Ensure all dependencies are installed using:
   ```bash
   pip install -r requirements.txt
   ```
2. **Error Loading Images**: Verify the file format and location.
3. **Unexpected Results**: Ensure you are marking areas properly and using a valid reference image.


For further assistance, please contact: [Tikusathwik@gmail.com]
