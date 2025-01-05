
# Advanced Freehand Drawing Tool with Histogram Matching

## **Overview**
This MATLAB-based application provides a GUI for freehand drawing with advanced features. It allows users to create drawings with customizable tools, perform histogram matching with reference images, edit their work, and save or load drawings. The tool is intuitive and suitable for creative projects and image editing tasks.

---

## **Features**
1. **Freehand Drawing**:
   - Adjustable brush size and color for precise drawing.
   - Interactive drawing using `drawfreehand`.

2. **Histogram Matching**:
   - Match the histogram of the drawing with a reference image.
   - Enhance tonal alignment for improved image quality.

3. **Undo and Reset**:
   - Undo the last action with a single click.
   - Reset the canvas to its original blank state.

4. **Save and Load Drawings**:
   - Save your drawing as an image file (*.jpg, *.png).
   - Load a saved drawing for further editing.

5. **User-Friendly GUI**:
   - Buttons, sliders, and labels for seamless interaction.

---

## **Installation**
### Prerequisites
- MATLAB R2018b or later (for `drawfreehand` support).
- Image Processing Toolbox (for `imhistmatch` and `createMask` functions).

### Steps
1. Download the project files.
2. Ensure MATLAB is installed on your system.
3. Open MATLAB and set the directory to the location of the project files.
4. Run the file `test.m` to start the application.

---

## **Usage**
### **Start the Application**
1. Launch MATLAB.
2. Run the command:
   ```matlab
   test
   ```

### **Drawing**
- Click the **"Draw"** button and use the mouse to draw on the canvas.
- Adjust the brush size using the **slider**.
- Select a brush color using the **"Select Color"** button.

### **Editing**
- **Undo**: Click the **"Undo"** button to revert the last action.
- **Reset**: Click the **"Reset"** button to clear the canvas.

### **Histogram Matching**
1. Click the **"Match Histogram"** button.
2. Select a reference image.
3. The histogram-matched image will be displayed in a new window.

### **Save and Load**
- **Save**: Click the **"Save Drawing"** button to export your drawing.
- **Load**: Click the **"Load Drawing"** button to import a saved drawing.

---

## **Code Structure**
### **Main Function**
- **`test`**: Initializes the GUI, sets up the canvas, and defines user interactions.

### **Key Functionalities**
1. **Drawing**:
   - `startDrawing`: Enables freehand drawing with adjustable tools.
2. **Histogram Matching**:
   - `matchHistogram`: Matches the histogram of the drawing with a reference image.
3. **Editing**:
   - `undoDrawing`: Reverts the last drawing action.
   - `resetCanvas`: Clears the canvas.
4. **File Operations**:
   - `saveDrawing`: Saves the current drawing to a file.
   - `loadDrawing`: Loads a saved drawing.

---

## **Future Enhancements**
1. **Enhanced Drawing Tools**:
   - Add eraser and shape-drawing tools.
   - Include a text tool for annotations.

2. **Color Support**:
   - Extend functionality for color images.
   - Implement advanced histogram matching for RGB images.

3. **Layer Management**:
   - Introduce multiple layers with adjustable transparency.

4. **Advanced Features**:
   - Add zoom, pan, and real-time collaboration.
   - Integrate AI tools for shape detection and handwriting recognition.

5. **Mobile Support**:
   - Adapt the application for touch gestures and mobile devices.

---

## **Known Issues**
1. **Unsupported MATLAB Versions**:
   - The `drawfreehand` function is not available in versions prior to R2018b.
   - Update MATLAB to a compatible version.

2. **Toolbox Requirement**:
   - Ensure the Image Processing Toolbox is installed for proper functionality.

---

## **Contribution**
Contributions are welcome! If you’d like to enhance the application or fix bugs:
1. Fork the repository.
2. Make your changes.
3. Submit a pull request.

---

## **License**
This project is licensed under the MIT License.

---

## **Acknowledgments**
- MATLAB documentation for GUI development.
- The MATLAB community for providing valuable insights into interactive graphics.
