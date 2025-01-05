import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageEnhance, ImageFilter, ImageTk

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Adjustment Tool")
        
        # Initial image setup
        self.image = None
        self.display_image = None
        
        # Create GUI elements
        self.create_gui()
    
    def create_gui(self):
        # Main frame for layout
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)

        # Left frame for image and control panel
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=10)

        # Canvas to display image
        self.canvas = tk.Canvas(left_frame, width=500, height=500, bg="gray")
        self.canvas.pack()

        # Right frame for controls
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, padx=10, sticky='n')

        # Open Image button
        open_button = tk.Button(right_frame, text="Open Image", command=self.open_image)
        open_button.grid(row=0, column=0, pady=5)

        # Resize controls
        tk.Label(right_frame, text="Resize Width:").grid(row=1, column=0, pady=5)
        self.width_entry = tk.Entry(right_frame, width=10)
        self.width_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(right_frame, text="Resize Height:").grid(row=2, column=0, pady=5)
        self.height_entry = tk.Entry(right_frame, width=10)
        self.height_entry.grid(row=2, column=1, pady=5)
        
        resize_button = tk.Button(right_frame, text="Resize", command=self.resize_image)
        resize_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Crop controls
        tk.Label(right_frame, text="Crop (left, top, right, bottom):").grid(row=4, column=0, columnspan=2, pady=5)
        self.crop_entries = [tk.Entry(right_frame, width=5) for _ in range(4)]
        for i, entry in enumerate(self.crop_entries):
            entry.grid(row=5, column=i, padx=2, pady=5)
        
        crop_button = tk.Button(right_frame, text="Crop", command=self.crop_image)
        crop_button.grid(row=6, column=0, columnspan=4, pady=5)

        # Rotate controls
        tk.Label(right_frame, text="Rotate Angle:").grid(row=7, column=0, pady=5)
        self.rotate_entry = tk.Entry(right_frame, width=10)
        self.rotate_entry.grid(row=7, column=1, pady=5)
        
        rotate_button = tk.Button(right_frame, text="Rotate", command=self.rotate_image)
        rotate_button.grid(row=8, column=0, columnspan=2, pady=5)

        # Brightness controls
        tk.Label(right_frame, text="Brightness (1.0 is normal):").grid(row=9, column=0, pady=5)
        self.brightness_scale = tk.Scale(right_frame, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL)
        self.brightness_scale.set(1)
        self.brightness_scale.grid(row=9, column=1, pady=5)
        
        brightness_button = tk.Button(right_frame, text="Apply Brightness", command=self.apply_brightness)
        brightness_button.grid(row=10, column=0, columnspan=2, pady=5)

        # Contrast controls
        tk.Label(right_frame, text="Contrast (1.0 is normal):").grid(row=11, column=0, pady=5)
        self.contrast_scale = tk.Scale(right_frame, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL)
        self.contrast_scale.set(1)
        self.contrast_scale.grid(row=11, column=1, pady=5)
        
        contrast_button = tk.Button(right_frame, text="Apply Contrast", command=self.apply_contrast)
        contrast_button.grid(row=12, column=0, columnspan=2, pady=5)

        # Color adjustment controls
        tk.Label(right_frame, text="Color (1.0 is normal):").grid(row=13, column=0, pady=5)
        self.color_scale = tk.Scale(right_frame, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL)
        self.color_scale.set(1)
        self.color_scale.grid(row=13, column=1, pady=5)
        
        color_button = tk.Button(right_frame, text="Apply Color", command=self.apply_color)
        color_button.grid(row=14, column=0, columnspan=2, pady=5)

        # Sharpness controls
        tk.Label(right_frame, text="Sharpness (1.0 is normal):").grid(row=15, column=0, pady=5)
        self.sharpness_scale = tk.Scale(right_frame, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL)
        self.sharpness_scale.set(1)
        self.sharpness_scale.grid(row=15, column=1, pady=5)
        
        sharpness_button = tk.Button(right_frame, text="Apply Sharpness", command=self.apply_sharpness)
        sharpness_button.grid(row=16, column=0, columnspan=2, pady=5)

        # Blur controls
        tk.Label(right_frame, text="Blur Radius:").grid(row=17, column=0, pady=5)
        self.blur_entry = tk.Entry(right_frame, width=10)
        self.blur_entry.grid(row=17, column=1, pady=5)
        
        blur_button = tk.Button(right_frame, text="Apply Blur", command=self.apply_blur)
        blur_button.grid(row=18, column=0, columnspan=2, pady=5)
    
    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.display_image = self.image.copy()
            self.update_canvas()
    
    def update_canvas(self):
        if self.display_image:
            self.tk_image = ImageTk.PhotoImage(self.display_image)
            self.canvas.create_image(250, 250, image=self.tk_image)

    def resize_image(self):
        if self.image:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            self.display_image = self.image.resize((width, height))
            self.update_canvas()

    def crop_image(self):
        if self.image:
            left = int(self.crop_entries[0].get())
            top = int(self.crop_entries[1].get())
            right = int(self.crop_entries[2].get())
            bottom = int(self.crop_entries[3].get())
            self.display_image = self.image.crop((left, top, right, bottom))
            self.update_canvas()

    def rotate_image(self):
        if self.image:
            angle = float(self.rotate_entry.get())
            self.display_image = self.image.rotate(angle)
            self.update_canvas()

    def apply_brightness(self):
        if self.image:
            enhancer = ImageEnhance.Brightness(self.image)
            self.display_image = enhancer.enhance(self.brightness_scale.get())
            self.update_canvas()

    def apply_contrast(self):
        if self.image:
            enhancer = ImageEnhance.Contrast(self.image)
            self.display_image = enhancer.enhance(self.contrast_scale.get())
            self.update_canvas()

    def apply_color(self):
        if self.image:
            enhancer = ImageEnhance.Color(self.image)
            self.display_image = enhancer.enhance(self.color_scale.get())
            self.update_canvas()

    def apply_sharpness(self):
        if self.image:
            enhancer = ImageEnhance.Sharpness(self.image)
            self.display_image = enhancer.enhance(self.sharpness_scale.get())
            self.update_canvas()

    def apply_blur(self):
        if self.image:
            radius = float(self.blur_entry.get())
            self.display_image = self.image.filter(ImageFilter.GaussianBlur(radius))
            self.update_canvas()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
