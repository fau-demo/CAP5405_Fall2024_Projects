import json
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import os


root = Tk()
root.title("Insta Filter Tool")
root.geometry("1000x700")


img = None
img_display = None
img_original = None  
img_filtered = None  
filters = []  


def load_filters():
    global filters
    with open("filters.json", "r") as f:
        filters = json.load(f)


def load_image():
    global img, img_display, img_original, img_filtered
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        img = Image.open(file_path)
        img_original = img.copy()  
        img_filtered = img.copy()  
        display_image(img)
        generate_filter_previews()  


def display_image(image):
    global img_display
    img_display = ImageTk.PhotoImage(image.resize((400, 400)))
    image_label.config(image=img_display)


def apply_filter(settings):
    global img_filtered, img_original
    img_filtered = img_original.copy()

    
    enhancer = ImageEnhance.Brightness(img_filtered)
    img_filtered = enhancer.enhance(settings["brightness"])

    
    enhancer = ImageEnhance.Contrast(img_filtered)
    img_filtered = enhancer.enhance(settings["contrast"])

    
    enhancer = ImageEnhance.Color(img_filtered)
    img_filtered = enhancer.enhance(settings["saturation"])

    
    if settings.get("grayscale", False):
        img_filtered = img_filtered.convert("L").convert("RGB")

    display_image(img_filtered)


def generate_filter_previews():
    for widget in filter_frame.winfo_children():
        widget.destroy()  # Clear previous previews

    for i, filter_settings in enumerate(filters):
        
        filter_container = Frame(filter_frame)
        filter_container.grid(row=i // 5, column=i % 5, padx=5, pady=5)

        
        preview_img_path = filter_settings.get("preview")
        if preview_img_path and os.path.exists(preview_img_path):
            preview_img = Image.open(preview_img_path)
            preview_img.thumbnail((100, 100))
            preview_img_tk = ImageTk.PhotoImage(preview_img)
        else:
            preview_img_tk = None

        
        btn = Button(filter_container, image=preview_img_tk, command=lambda s=filter_settings: set_filter_and_sliders(s))
        btn.image = preview_img_tk  
        btn.pack()

        
        Label(filter_container, text=filter_settings["name"]).pack()


def set_filter_and_sliders(settings):
    brightness_slider.set(settings["brightness"])
    contrast_slider.set(settings["contrast"])
    saturation_slider.set(settings["saturation"])
    grayscale_var.set(1 if settings.get("grayscale", False) else 0)
    apply_filters()


def apply_filters(*args):
    settings = {
        "brightness": brightness_slider.get(),
        "contrast": contrast_slider.get(),
        "saturation": saturation_slider.get(),
        "grayscale": bool(grayscale_var.get())
    }
    apply_filter(settings)


def save_image():
    if img_filtered:
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        if file_path:
            img_filtered.save(file_path)

# Scrollable Frame class
class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        
        self.canvas = Canvas(self)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


scrollable_frame = ScrollableFrame(root)
scrollable_frame.pack(fill="both", expand=True)


image_label = Label(scrollable_frame.scrollable_frame)
image_label.pack()

load_btn = Button(scrollable_frame.scrollable_frame, text="Load Image", command=load_image)
load_btn.pack()

save_btn = Button(scrollable_frame.scrollable_frame, text="Save Image", command=save_image)
save_btn.pack()


filter_frame = Frame(scrollable_frame.scrollable_frame)
filter_frame.pack(pady=10)


brightness_slider = Scale(scrollable_frame.scrollable_frame, from_=0.1, to=2.0, resolution=0.1, orient=HORIZONTAL, label="Brightness", command=apply_filters)
brightness_slider.set(1.0)
brightness_slider.pack()

contrast_slider = Scale(scrollable_frame.scrollable_frame, from_=0.1, to=2.0, resolution=0.1, orient=HORIZONTAL, label="Contrast", command=apply_filters)
contrast_slider.set(1.0)
contrast_slider.pack()

saturation_slider = Scale(scrollable_frame.scrollable_frame, from_=0.1, to=2.0, resolution=0.1, orient=HORIZONTAL, label="Saturation", command=apply_filters)
saturation_slider.set(1.0)
saturation_slider.pack()

grayscale_var = IntVar()
grayscale_checkbox = Checkbutton(scrollable_frame.scrollable_frame, text="Grayscale", variable=grayscale_var, command=apply_filters)
grayscale_checkbox.pack()


load_filters()

root.mainloop()
