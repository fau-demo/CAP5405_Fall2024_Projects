import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Define the main application class
class HistogramMatchingApp:
    def __init__(self, root):
        """
        Initializes the GUI components and sets up the application layout.
        """
        self.root = root
        self.root.title("Histogram Matching Tool")

        # Create a frame to display images
        self.image_frame = tk.Frame(root)
        self.image_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Create a frame to display histograms
        self.histogram_frame = tk.Frame(root)
        self.histogram_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Add labels for image categories
        self.source_label = tk.Label(self.image_frame, text="Original")
        self.source_label.grid(row=0, column=0)

        self.target_label = tk.Label(self.image_frame, text="Reference")
        self.target_label.grid(row=0, column=1)

        self.result_label = tk.Label(self.image_frame, text="Result")
        self.result_label.grid(row=0, column=2)

        # Create canvases to display images
        self.source_canvas = tk.Canvas(self.image_frame, width=300, height=300, bg="white")
        self.source_canvas.grid(row=1, column=0)

        self.target_canvas = tk.Canvas(self.image_frame, width=300, height=300, bg="white")
        self.target_canvas.grid(row=1, column=1)

        self.result_canvas = tk.Canvas(self.image_frame, width=300, height=300, bg="white")
        self.result_canvas.grid(row=1, column=2)

        # Buttons for loading images and applying histogram matching
        self.load_source_btn = tk.Button(root, text="Load Original Image", command=self.load_source_image)
        self.load_source_btn.grid(row=1, column=0)

        self.load_target_btn = tk.Button(root, text="Load Reference Image", command=self.load_target_image)
        self.load_target_btn.grid(row=1, column=1)

        self.apply_btn = tk.Button(root, text="Apply Histogram Matching", command=self.apply_histogram_matching)
        self.apply_btn.grid(row=1, column=2)

        # Initialize placeholders for the source, target, and result images
        self.source_image = None
        self.target_image = None
        self.result_image = None

        # Set up a Matplotlib figure for displaying histograms
        self.figure, self.axes = plt.subplots(1, 3, figsize=(12, 4))
        self.figure.suptitle("Histograms: Original, Reference, and Result", fontsize=14)
        self.canvas = FigureCanvasTkAgg(self.figure, self.histogram_frame)
        self.canvas.get_tk_widget().pack()

    def load_source_image(self):
        """
        Loads the original image using a file dialog.
        """
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if filepath:
            self.source_image = cv2.imread(filepath)
            self.source_image = cv2.cvtColor(self.source_image, cv2.COLOR_BGR2RGB)
            self.display_image(self.source_image, self.source_canvas)

    def load_target_image(self):
        """
        Loads the reference image using a file dialog.
        """
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if filepath:
            self.target_image = cv2.imread(filepath)
            self.target_image = cv2.cvtColor(self.target_image, cv2.COLOR_BGR2RGB)
            self.display_image(self.target_image, self.target_canvas)

    def apply_histogram_matching(self):
        """
        Applies histogram matching to align the tonal distribution of the original image to the reference image.
        """
        if self.source_image is None or self.target_image is None:
            messagebox.showerror("Error", "Load both Original and Reference images!")
            return

        # Resize the target image to match the dimensions of the source image
        target_resized = cv2.resize(self.target_image, (self.source_image.shape[1], self.source_image.shape[0]))

        # Perform histogram matching
        self.result_image = self.histogram_matching(self.source_image, target_resized)

        # Display the result image
        self.display_image(self.result_image, self.result_canvas)

        # Update the histograms for all images
        self.update_histograms()

    @staticmethod
    def histogram_matching(source, target):
        """
        Matches the histogram of the source image to that of the target image.

        Args:
            source: Source image (original).
            target: Target image (reference).

        Returns:
            Histogram-matched image.
        """
        # Convert both images to LAB color space
        source_lab = cv2.cvtColor(source, cv2.COLOR_RGB2LAB)
        target_lab = cv2.cvtColor(target, cv2.COLOR_RGB2LAB)

        # Split the channels of the LAB color space
        src_l, src_a, src_b = cv2.split(source_lab)
        tgt_l, tgt_a, tgt_b = cv2.split(target_lab)

        # Match histograms for the L (luminance) channel
        src_l = HistogramMatchingApp.match_histograms(src_l, tgt_l)

        # Merge the channels back and convert to RGB
        matched_lab = cv2.merge([src_l, src_a, src_b])
        matched_rgb = cv2.cvtColor(matched_lab, cv2.COLOR_LAB2RGB)
        return matched_rgb

    @staticmethod
    def match_histograms(src, tgt):
        """
        Matches the histogram of one channel (source) to another channel (target).

        Args:
            src: Source channel.
            tgt: Target channel.

        Returns:
            The source channel with a matched histogram.
        """
        # Compute histograms and cumulative distribution functions (CDFs)
        hist_src, bins = np.histogram(src.ravel(), 256, [0, 256])
        hist_tgt, _ = np.histogram(tgt.ravel(), 256, [0, 256])

        cdf_src = np.cumsum(hist_src) / hist_src.sum()
        cdf_tgt = np.cumsum(hist_tgt) / hist_tgt.sum()

        # Create a lookup table to match CDFs
        lookup_table = np.interp(cdf_src, cdf_tgt, np.arange(256))
        matched = cv2.LUT(src, lookup_table.astype(np.uint8))
        return matched

    def display_image(self, image, canvas):
        """
        Displays the given image on the specified Tkinter canvas.

        Args:
            image: Image to display (numpy array).
            canvas: Tkinter canvas to display the image on.
        """
        img = Image.fromarray(image)
        img = img.resize((300, 300))  # Resize for better display in the GUI
        img_tk = ImageTk.PhotoImage(img)
        canvas.image = img_tk
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    def update_histograms(self):
        """
        Updates the histograms for the original, reference, and result images.
        """
        # Clear previous histograms
        self.axes[0].clear()
        self.axes[1].clear()
        self.axes[2].clear()

        # Plot the histogram for the original image
        if self.source_image is not None:
            for i, color in enumerate(['red', 'green', 'blue']):
                hist = cv2.calcHist([self.source_image], [i], None, [256], [0, 256])
                self.axes[0].plot(hist, color=color)
            self.axes[0].set_title("Original Image Histogram")

        # Plot the histogram for the reference image
        if self.target_image is not None:
            for i, color in enumerate(['red', 'green', 'blue']):
                hist = cv2.calcHist([self.target_image], [i], None, [256], [0, 256])
                self.axes[1].plot(hist, color=color)
            self.axes[1].set_title("Reference Image Histogram")

        # Plot the histogram for the result image
        if self.result_image is not None:
            for i, color in enumerate(['red', 'green', 'blue']):
                hist = cv2.calcHist([self.result_image], [i], None, [256], [0, 256])
                self.axes[2].plot(hist, color=color)
            self.axes[2].set_title("Result Image Histogram")

        # Refresh the canvas to display updated histograms
        self.canvas.draw()


if __name__ == "__main__":
    # Create and run the GUI application
    root = tk.Tk()
    app = HistogramMatchingApp(root)
    root.mainloop()
