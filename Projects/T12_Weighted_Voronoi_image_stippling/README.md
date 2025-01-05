# Stipple Image Generator App with GUI using Weighted Voronoi Stippling

**Weighted Voronoi Stippling** application with custom `customtkinter` GUI allows users to select an image, set stippling parameters, generate weighted Voronoi stippling diagrams, and save GIF of centroid evolution

![Untitled](https://github.com/user-attachments/assets/3669bfc0-6c92-4764-bc6d-41e02d860eca)


![banana_voronoi_stippled_9000_50](https://github.com/user-attachments/assets/db40ba79-e2c6-4c23-9b4f-6ede82ccdff3)


---

## 🌟 **Features**

- **File Selection**:
  - Supports different dimmensions
  - Supports different image types (Gray, Color etc)
  - file types:
    - `.png`
    - `.jpg`
    - `.jpeg`
    - `.bmp`
- **Plot Outputs**:
  - Produce weighted Voronoi diagram based on input image and paramerters
  - Produce stipple image based on the weighted Voronoi and input paramerters
- **Evolution GIF**:
  - Saves every iteration of image generation as a seemless GIF file showcasing centroid evolution
- **Quantization Levels**:
  - Can reduce the number of gray value outputs that are being used during computiation
- **Two Voronoi Region Centroid Computation Methods**:
  - Random sampling (Recommended):
    - Uses random sample of  `(max_x - min_x) * (max_y - min_y) * 10` size to find contained pixels, and uses those to compute gray value density centroid
    - Relativly faster Iterations
    - Introduces jitter, which is able to dislodge points that were previously stuck in an un-optimal space
  - Original Lloyd's Method:
    - Uses all pixels within region to compute gray value density centroid
    - Need fewer iterations to get to final Voronoi points
    - Final Voronoi points may be unevenly concentrated and result in some areas containing dense clusters of stuck points
- **Continuous Progression Report**:
  - Console logs updates after completion on each iteration and major code segment


---
## 🎓 **Instructions**

1. **Start Application:**
   - For windows, simply download and run `Weighted Voronoi Stippling.exe` executable
   - Otherwise download all `.py` files and use python to run `Voronoi_Gui.py`

2. **Select Image File:**:
   - Click `Browse` button and select an image file in your directory
     - ![image](https://github.com/user-attachments/assets/36764f16-38ac-418d-82d8-6efdee54c2d5)
   - Image preview should be available once selected
     - ![image](https://github.com/user-attachments/assets/df5c0541-a57f-41a7-9ee0-fb20aaf98d8c)
       
3. **Set Desired Parameters:**
   - ![image](https://github.com/user-attachments/assets/219baf1c-54b5-4f0d-8d76-3d7234071104)
     
4. **Start Voronoi Stipple Genoration:**:
  - ![image](https://github.com/user-attachments/assets/e62b09d1-eaaa-4fd0-a29c-58fa50652f83)
  
5. **Keep Track of Progression Through Console**
   - ![image](https://github.com/user-attachments/assets/87d2de32-83c0-4cb9-9576-cd8e918243dc)
6. **Output Figures:**
   - If the plot parameters are selected then the application should output three windows containing:
     - Final Voronoi Diagram with tessellations
     - Final Stipple Image
     - Original Image for reference
   - ![image](https://github.com/user-attachments/assets/306ef6c9-e086-4d27-a54f-3944b0ea99f9)
7. **Saved Evolution GIF:**
   - If the `Save` checkbox parameter is checked, the final saved evolution gif can be found in the same directory as `Weighted Voronoi Stippling.exe`/`Voronoi_Gui.py`
     
       -![image](https://github.com/user-attachments/assets/0c12f2a2-d93f-4274-a10d-0b6da211e2a3)
   - ![cameraman_voronoi_stippled_8000_30](https://github.com/user-attachments/assets/9c0ad0dc-4052-4c55-b2b1-4117fbbade15)


---

## 🚀 **Parameter Controls**

- **Select Image**:
  - Choose an image file (`.png`, `.jpg`, `.jpeg`, `.bmp`)
- **Stipple Points**:
  - Set the number of points for stippling (100 to 50,000)
- **Lloyd Iterations**:
  - Number of Lloyd relaxation iterations (0 to 100)
- **Quantization Levels** (optional):
  - Set number of gray values to interpret image as
- **Custom Seed** (optional):
  - Set custom seed for testing
- **Random Sampling** (Defualt: True):
  - Compute centroid using random sample instead of all pixels in region
- **Plot** (Defualt: True):
  - Show Voronoi diagram and stipple image results
- **Save** (Defualt: False):
  - Save evolution of Voronoi stipple through iterations in a GIF file


---

## 🛠️ Requirements

- Built and Tested using Python 3.13.1
- Required Python Libraries:
  - `skimage`
  - `PIL`
  - `matplotlib`
  - `numpy`
  - `scipy`
  - `customtkinter`

---

## 📋 References

The following were influencial to the creating of this application
- Weighted Voronoi Stippling, Adrian Secord
  - https://www.cs.ubc.ca/labs/imager/tr/2002/secord2002b/secord.2002b.pdf
- `customtkinter` GUI library
  - https://github.com/TomSchimansky/CustomTkinter
- The Conding Train's P5.js that also references Adrian Secord's paper
  - https://www.youtube.com/watch?v=Bxdt6T_1qgc
 
---
