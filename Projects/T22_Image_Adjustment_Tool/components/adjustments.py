from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from io import BytesIO
import numpy as np


class Adjustments:
    def __init__(self, image_viewer, history):
        self.image_viewer = image_viewer
        self.history = history
        self.original_image = None
        self.current_image = None
        self.brightness_factor = 1.0
        self.contrast_factor = 1.0
        self.saturation_factor = 1.0
        self.sharpness_factor = 1.0
        self.exposure_factor = 1.0

    def load_image(self):
        """Load the image from the pixmap into PIL format."""

        # Convert QPixmap to QImage
        q_image = self.image_viewer.pixmap.toImage()
        
        # Extract the image buffer
        buffer = q_image.bits()
        buffer.setsize(q_image.byteCount())
        
        # Convert the QImage to a NumPy array
        width = q_image.width()
        height = q_image.height()
        format = q_image.format()
        
        if format == QImage.Format_RGB32:
            # For RGB32 format, the buffer needs to be reshaped as (height, width, 4)
            image_array = np.array(buffer).reshape(height, width, 4)
            # Discard the alpha channel
            image_array = image_array[..., :3][..., ::-1]
        elif format == QImage.Format_RGB888:
            # For RGB888 format, the buffer is already RGB
            image_array = np.array(buffer).reshape(height, width, 3)[..., ::-1]
        else:
            raise ValueError(f"Unsupported QImage format: {format}")
        
        self.original_image = Image.fromarray(image_array, mode="RGB")
        self.current_image = self.original_image.copy()
        self.history.save_to_history(self.original_image)

    def apply_adjustments(self, adjustment=None):
        """Apply adjustments to the downscaled preview image."""
        if not self.original_image:
            return

        adjusted_image = self.original_image.copy()

        # Apply adjustments
        adjusted_image = ImageEnhance.Brightness(adjusted_image).enhance(self.brightness_factor)
        adjusted_image = ImageEnhance.Contrast(adjusted_image).enhance(self.contrast_factor)
        adjusted_image = ImageEnhance.Color(adjusted_image).enhance(self.saturation_factor)
        adjusted_image = ImageEnhance.Sharpness(adjusted_image).enhance(self.sharpness_factor)
        adjusted_image = adjusted_image.point(lambda p: p * (1 + self.exposure_factor))

        # Update the current image and display it
        self.current_image = adjusted_image
        self.history.save_to_history(self.current_image)
        self.update_image_viewer()

    def adjust_brightness(self, value):
        """Adjust brightness based on slider value."""
        self.brightness_factor = 1 + (value / 100)
        self.apply_adjustments(adjustment="brightness")

    def adjust_contrast(self, value):
        """Adjust contrast based on slider value."""
        self.contrast_factor = (value / 10)
        self.apply_adjustments(adjustment="contrast")

    def adjust_saturation(self, value):
        """Adjust saturation based on slider value."""
        self.saturation_factor = (value / 10)
        self.apply_adjustments(adjustment="saturation")

    def adjust_sharpness(self, value):
        """Adjust sharpness based on slider value."""
        self.sharpness_factor = (value / 10)
        self.apply_adjustments(adjustment="sharpness")
    
    def adjust_exposure(self, value):
        """Adjust exposure based on slider value."""
        self.exposure_factor = (value / 100)
        self.apply_adjustments(adjustment="exposure")

    def update_image_viewer(self):
        """Update the image viewer with the current adjusted image."""
        if not self.current_image:
            return

        # Convert the PIL Image to RGB mode if it is not in RGB
        rgb_image = self.current_image.convert("RGB")
        data = rgb_image.tobytes("raw", "RGB")
        
        # Create a QImage from the byte data and set the pixmap with it
        q_image = QImage(
            data, rgb_image.width, rgb_image.height, QImage.Format_RGB888
        )
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(
            self.image_viewer.size(), 
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.image_viewer.pixmap = scaled_pixmap
        self.image_viewer.setPixmap(scaled_pixmap)

    def apply_grayscale_filter(self):
        """Apply a grayscale filter to the image."""
        if self.original_image:
            self.current_image = ImageOps.grayscale(self.original_image).convert("RGB")
            self.history.save_to_history(self.current_image)
            self.update_image_viewer()

    def apply_sepia_filter(self):
        """Apply a sepia filter to the image."""
        if self.original_image:
            sepia_filter = self.original_image.convert("RGB")
            sepia_array = np.array(sepia_filter)
            tr = (sepia_array[..., 0] * 0.393 + sepia_array[..., 1] * 0.769 + sepia_array[..., 2] * 0.189).clip(0, 255)
            tg = (sepia_array[..., 0] * 0.349 + sepia_array[..., 1] * 0.686 + sepia_array[..., 2] * 0.168).clip(0, 255)
            tb = (sepia_array[..., 0] * 0.272 + sepia_array[..., 1] * 0.534 + sepia_array[..., 2] * 0.131).clip(0, 255)
            sepia_image = np.stack([tr, tg, tb], axis=-1).astype("uint8")
            self.current_image = Image.fromarray(sepia_image)
            self.history.save_to_history(self.current_image)
            self.update_image_viewer()

    def apply_invert_filter(self):
        """Apply an invert filter to the image."""
        if self.original_image:
            self.current_image = ImageOps.invert(self.original_image)
            self.history.save_to_history(self.current_image)
            self.update_image_viewer()

    def apply_cool_tone_filter(self):
        """
        Apply a cool tone filter by blending the image with a blue tint overlay.
        """
        if self.original_image:
            overlay = Image.new("RGB", self.original_image.size, (173, 216, 230))
            self.current_image = Image.blend(self.original_image, overlay, alpha=0.2)
            self.history.save_to_history(self.current_image)
            self.update_image_viewer()

    
    def apply_bright_glow_filter(self):
        """Apply a bright glow filter to the image."""
        if self.original_image:
            glow_image = ImageEnhance.Brightness(self.original_image).enhance(1.5)
            self.current_image = glow_image.filter(ImageFilter.GaussianBlur(radius=2))
            self.history.save_to_history(self.current_image)
            self.update_image_viewer()