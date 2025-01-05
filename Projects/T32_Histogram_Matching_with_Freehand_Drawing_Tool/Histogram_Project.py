import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import cv2
import numpy as np


class HistogramMatchingApp:
    """
    A GUI application for histogram matching with a freehand drawing tool.
    Reference:
    - OpenCV Documentation: https://docs.opencv.org/
    - Pillow (PIL) Documentation: https://pillow.readthedocs.io/
    - Tkinter Documentation: https://docs.python.org/3/library/tkinter.html
    """

    def __init__(self, root):
        # Initialize the main application window and GUI components
        self.root = root
        self.root.title("Histogram Matching with Freehand Drawing")

        # Set canvas dimensions for image display
        self.canvas_width = 800
        self.canvas_height = 600

        # Create a canvas for image display and drawing
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side=tk.LEFT)

        # Frame for buttons and controls
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Button to load target image
        self.load_button = tk.Button(self.controls_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)

        # Button to load reference image for histogram matching
        self.load_reference_button = tk.Button(self.controls_frame, text="Load Reference Image", command=self.load_reference_image)
        self.load_reference_button.pack(pady=10)

        # Button to process the image with histogram matching
        self.process_button = tk.Button(self.controls_frame, text="Process", command=self.process_image)
        self.process_button.pack(pady=10)

        # Button to clear any freehand drawings on the canvas
        self.clear_button = tk.Button(self.controls_frame, text="Clear Drawing", command=self.clear_drawing)
        self.clear_button.pack(pady=10)

        # Button to export the processed image to a file
        self.export_button = tk.Button(self.controls_frame, text="Export Result", command=self.export_image)
        self.export_button.pack(pady=10)

        # Initialize variables for storing image data and drawing state
        self.image = None  # Original image to process
        self.reference_image = None  # Reference image for histogram matching
        self.drawing = False  # Indicates if user is drawing
        self.drawn_mask = None  # Mask to track user-drawn areas
        self.start_x = None  # Starting x-coordinate for drawing
        self.start_y = None  # Starting y-coordinate for drawing

        # Bind mouse events to drawing actions on the canvas
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    def load_image(self):
        """
        Load the target image to be processed. Supported formats: JPG, PNG.
        """
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if not filepath:
            return

        # Load the image using PIL and convert to RGB
        self.image = Image.open(filepath).convert("RGB")
        self.display_image()

    def load_reference_image(self):
        """
        Load the reference image for histogram matching.
        """
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if not filepath:
            return

        # Load the reference image using PIL and convert to RGB
        self.reference_image = Image.open(filepath).convert("RGB")
        messagebox.showinfo("Info", "Reference image loaded successfully!")

    def display_image(self):
        """
        Display the current image on the canvas, resizing it to fit the canvas size.
        """
        if self.image:
            # Resize and display the image on the canvas
            self.tk_image = ImageTk.PhotoImage(self.image.resize((self.canvas_width, self.canvas_height)))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

            # Initialize a blank mask for drawing (used for histogram matching)
            self.drawn_mask = Image.new("L", (self.image.width, self.image.height), 0)

    def start_draw(self, event):
        """
        Start drawing on the canvas.
        """
        self.drawing = True
        self.start_x = event.x
        self.start_y = event.y

    def draw(self, event):
        """
        Draw on the canvas while the mouse is being dragged.
        """
        if self.drawing and self.image:
            # Draw a line on the canvas
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill="black", width=3)
            draw = ImageDraw.Draw(self.drawn_mask)

            # Scale the drawing coordinates to match the image size
            scale_x = self.image.width / self.canvas_width
            scale_y = self.image.height / self.canvas_height

            # Draw on the mask for histogram matching
            draw.line((self.start_x * scale_x, self.start_y * scale_y, event.x * scale_x, event.y * scale_y), fill=255, width=10)

            # Update the starting coordinates for the next segment
            self.start_x = event.x
            self.start_y = event.y

    def end_draw(self, event):
        """
        Stop drawing when the mouse button is released.
        """
        self.drawing = False

    def clear_drawing(self):
        """
        Clear the canvas and reset the mask for new drawings.
        """
        self.canvas.delete("all")
        self.display_image()

    def process_image(self):
        """
        Apply histogram matching to the selected region of the image.
        """
        if self.image and self.reference_image and self.drawn_mask:
            # Convert images to OpenCV format (numpy arrays)
            img = np.array(self.image)
            ref = np.array(self.reference_image)
            mask = np.array(self.drawn_mask)

            # Resize the reference image to match the target image's dimensions
            ref = cv2.resize(ref, (img.shape[1], img.shape[0]))

            # Perform histogram matching
            result = self.histogram_match(img, ref, mask)

            # Update the image with the processed result
            self.image = Image.fromarray(result)
            self.display_image()

    def histogram_match(self, source, reference, mask):
        """
        Perform histogram matching between the source and reference images using the mask.
        """
        # Convert images to LAB color space
        source_lab = cv2.cvtColor(source, cv2.COLOR_RGB2LAB)
        reference_lab = cv2.cvtColor(reference, cv2.COLOR_RGB2LAB)

        # Match histograms for each LAB channel
        for i in range(3):
            # Calculate histograms with the mask
            source_hist = cv2.calcHist([source_lab], [i], mask, [256], [0, 256])
            reference_hist = cv2.calcHist([reference_lab], [i], None, [256], [0, 256])

            # Compute cumulative distribution functions (CDFs)
            cdf_source = np.cumsum(source_hist / np.sum(source_hist))
            cdf_reference = np.cumsum(reference_hist / np.sum(reference_hist))

            # Create a lookup table
            lut = np.interp(cdf_source, cdf_reference, np.arange(256))

            # Apply LUT to the source image
            source_lab[:, :, i] = cv2.LUT(source_lab[:, :, i], lut.astype('uint8'))

        # Convert back to RGB
        return cv2.cvtColor(source_lab, cv2.COLOR_LAB2RGB)

    def export_image(self):
        """
        Export the processed image to a file.
        """
        if self.image:
            filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if filepath:
                # Save the image to the specified location
                self.image.save(filepath)
                messagebox.showinfo("Info", "Image exported successfully!")


# Main entry point for the application
if __name__ == "__main__":
    # Initialize and run the Tkinter application
    root = tk.Tk()
    app = HistogramMatchingApp(root)
    root.mainloop()
