# Edinity: A Feature-Rich Photo Editing Application

Welcome to **Edinity**, a user-friendly photo editing application designed to provide intuitive image manipulation tools and a sleek interface. With Edinity, users can upload, edit, and enhance their images seamlessly through an elegant GUI.

---

## **Project Details**

- **Team Members**: 
  - Mani Teja Rayana          --> Z23740179
  - Shilpa Karedla            --> Z23746751
  - Siva Shankar Yaddanapudi  --> Z23748872

- **Software Used**: 
  - Python 3.8 or higher
  - Tkinter (for GUI)
  - Pillow (for image processing)

---

## **Features**

### **Core Functionality**
- **Image Upload and Selection**:
  - Upload images from local storage or select existing files from a gallery.
- **Editing Tools**:
  - Crop, Adjust (Brightness, Contrast, etc.), Filters, Effects, and Reset.
- **Undo/Redo Options**:
  - Easily reverse or reapply edits.
- **Navigation**:
  - Transition between screens using Home, Hamburger Menu, and other navigation buttons.

### **User Interface**
- **Splash Screen**:
  - Welcomes the user and transitions to the Home Screen.
- **Home Screen**:
  - Provides options to upload an image and navigate to the editing screen.
- **Editing Screen**:
  - Central area to display the uploaded image.
  - Toolbar with semi-transparent buttons resembling a Windows-style interface.

---

## **Folder Structure**

```plaintext
Edinity/
├── src/
│   ├── main.py                 # Entry point of the application
│   ├── splash_screen.py        # Splash screen functionality
│   ├── home_screen.py          # Home screen functionality
│   ├── editing_screen.py       # Editing screen and tools
│   └── utilities.py          # Reusable helper functions
├── assets/
│   ├── beauty.png              # Beauty icon
│   ├── circular.png            # Circular icon
│   ├── controller.png          # Controller icon
│   ├── Create.Enhance.Inspire..png # Branding image
│   ├── crop.png                # Crop tool icon
│   ├── ediNity.png             # Branding logo
│   ├── filter.png              # Filter tool icon
│   ├── image.png               # Placeholder for images
│   ├── logo_head.png           # Application logo
│   ├── lone-tree.jpg           # Sample image
│   └── upload.png              # Upload icon
├── docs/
│   ├── README.md               # Project overview
├── requirements.txt            # Python dependencies
├── .gitignore                  # Files to exclude from Git tracking
└── LICENSE                     # License file
```

---

## **Installation and Running the Program**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ManitejaRayana/Edinity.git
   cd Edinity
   ```

2. **Set Up Dependencies**:
   Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python src/main.py
   ```

4. **Expected Output**:
   - On launching the program, the Splash Screen will appear.
   - After transitioning, users will reach the Home Screen to upload images.
   - Once an image is uploaded, it will open in the Editing Screen, displaying various editing tools and options.

---

## **Input Image Requirements**

- **Format**: JPEG, PNG
- **Size**: Up to 5MB
- **Resolution**: Minimum 300x300 pixels for optimal results

---

## **Supported Operating Systems**

- Windows
- Linux

---

## **Dependencies**

The following Python libraries are required for Edinity:
- `tkinter` (GUI framework)
- `Pillow` (Image processing)

Install them via the `requirements.txt` file or manually:
```bash
pip install pillow
```

---

## **References and Resources**

- Tkinter Documentation: https://docs.python.org/3/library/tkinter.html
- Pillow Documentation: https://pillow.readthedocs.io/en/stable/
- Python Official Website: https://www.python.org/

---

## **License**

This project is licensed under the [MIT License](LICENSE).

---

## **Contact**

If you have any questions or suggestions, feel free to reach out:
- **Email**: maniteja.rayana@gmail.com
- **GitHub**: [https://github.com/yourusername](https://github.com/yourusername)

---

## **Screenshots**

### Home Screen:
![Home Screen](assets\HomeScreen.png)

### Editing Screen:
![Editing Screen](assets/editingScreen.png)

---

Thank you for using Edinity! We hope you enjoy editing your photos effortlessly!

