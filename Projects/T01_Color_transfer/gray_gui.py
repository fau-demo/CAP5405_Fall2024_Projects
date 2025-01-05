import cv2
import numpy as np
from tkinter import Tk, Button, Label, filedialog, messagebox, Frame
from PIL import Image, ImageTk

# Define a class for the Color Transfer Application
class ColorTransferApp:
    def __init__(self, root):
        """
        Initialize the GUI application, set up the layout, and define variables.
        :param root: The root Tkinter window.
        """
        self.root = root
        self.root.title("Color Palette Transfer Tool") # Set the window title
        self.root.geometry("1200x500") # Set the window dimensions

        self.base_image_path = None
        self.target_image_path = None

        # Frames for layout
        self.image_frame = Frame(self.root)
        self.image_frame.pack(pady=10)

        # Base image display
        self.base_image_label = Label(self.image_frame, text="Base Image")
        self.base_image_label.grid(row=0, column=0, padx=20)
        self.base_canvas = Label(self.image_frame)
        self.base_canvas.grid(row=1, column=0, padx=20)

        # Target image display
        self.target_image_label = Label(self.image_frame, text="Target Image")
        self.target_image_label.grid(row=0, column=1, padx=20)
        self.target_canvas = Label(self.image_frame)
        self.target_canvas.grid(row=1, column=1, padx=20)

        # Result image display
        self.result_image_label = Label(self.image_frame, text="Result Image")
        self.result_image_label.grid(row=0, column=2, padx=20)
        self.result_canvas = Label(self.image_frame)
        self.result_canvas.grid(row=1, column=2, padx=20)

        # Buttons for file selection and processing
        self.select_base_button = Button(self.root, text="Select Base Image", command=self.select_base_image)
        self.select_base_button.pack(pady=5)

        self.select_target_button = Button(self.root, text="Select Target Image", command=self.select_target_image)
        self.select_target_button.pack(pady=5)

        self.transfer_button = Button(self.root, text="Apply Color Transfer", command=self.transfer_colors)
        self.transfer_button.pack(pady=20)

    def load_image(self, path, canvas, width=300, height=200):
        """
        Load and display an image in the specified canvas.
        :param path: File path of the image.
        :param canvas: Tkinter canvas to display the image.
        :param width: Width to resize the image for display.
        :param height: Height to resize the image for display.
        """
        img = cv2.imread(path)
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            img = Image.fromarray(img)
            img = img.resize((width, height))  # Resize for display
            img_tk = ImageTk.PhotoImage(img)
            canvas.config(image=img_tk)
            canvas.image = img_tk  # Keep a reference to prevent garbage collection

    def select_base_image(self):
        """
        Allow the user to select the base image and display it.
        """
        self.base_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])
        if self.base_image_path:
            self.base_image_label.config(text="Base Image")
            self.load_image(self.base_image_path, self.base_canvas)
        else:
            self.base_image_label.config(text="Base Image: Not selected")

    def select_target_image(self):
        """
        Allow the user to select the target image and display it.
        """
        self.target_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])
        if self.target_image_path:
            self.target_image_label.config(text="Target Image")
            self.load_image(self.target_image_path, self.target_canvas)
        else:
            self.target_image_label.config(text="Target Image: Not selected")

    def transfer_colors(self):
        """
        Perform the color transfer operation from the base image to the target image.
        """
        if not self.base_image_path or not self.target_image_path:
            messagebox.showerror("Error", "Please select both base and target images.")
            return

        # Read and process the images
        base_img = cv2.imread(self.base_image_path)
        target_img = cv2.imread(self.target_image_path)

        if base_img is None or target_img is None:
            messagebox.showerror("Error", "Error reading images. Ensure the files are valid image formats.")
            return

        # Convert images to LAB color space
        base_lab = cv2.cvtColor(base_img, cv2.COLOR_BGR2LAB).astype("float32")
        target_lab = cv2.cvtColor(target_img, cv2.COLOR_BGR2LAB).astype("float32")

        # Compute the mean and standard deviation of LAB channels
        base_mean, base_std = cv2.meanStdDev(base_lab)
        target_mean, target_std = cv2.meanStdDev(target_lab)

        # Reshape to (1, 1, 3) for broadcasting
        base_mean = base_mean.reshape((1, 1, 3))
        base_std = base_std.reshape((1, 1, 3))
        target_mean = target_mean.reshape((1, 1, 3))
        target_std = target_std.reshape((1, 1, 3))

        # Perform color transfer
        result_lab = ((target_lab - target_mean) / target_std) * base_std + base_mean
        result_lab = np.clip(result_lab, 0, 255).astype("uint8")
        result_bgr = cv2.cvtColor(result_lab, cv2.COLOR_LAB2BGR)

        # Convert result to ImageTk for GUI preview
        result_image = Image.fromarray(cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB))
        result_image = result_image.resize((300, 200))  # Resize for display
        result_photo = ImageTk.PhotoImage(result_image)
        self.result_canvas.config(image=result_photo)
        self.result_canvas.image = result_photo  # Keep a reference

        # Save the result
        result_path = "result_color_transfer.jpg"
        cv2.imwrite(result_path, result_bgr)
        messagebox.showinfo("Success", f"Color transfer completed! Result saved as {result_path}")


if __name__ == "__main__":
    # Create the Tkinter root window
    root = Tk()
    # Create an instance of the application
    app = ColorTransferApp(root)
    # Run the Tkinter event loop
    root.mainloop()
