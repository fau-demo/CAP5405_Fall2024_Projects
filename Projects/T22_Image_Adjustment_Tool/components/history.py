from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class History:
    def __init__(self, image_viewer):
        self.image_viewer = image_viewer
        self.history = []
        self.redo_stack = []

    def undo(self):
        """Undo the last action."""
        if len(self.history) >= 2:
            self.current_image = self.history.pop()
            self.redo_stack.append(self.current_image)
            self.current_image = self.history[-1] if self.history else None
            self.update_viewer()

    def redo(self):
        """Redo the last undone action."""
        if self.redo_stack:
            self.current_image = self.redo_stack.pop()
            self.history.append(self.current_image)
            self.update_viewer()

    def save_to_history(self, image):
        """Save the current state to history for undo/redo functionality."""
        if image is not None:
            self.history.append(image)
            self.redo_stack.clear()

    def update_viewer(self):
        """Update the image viewer with the current adjusted image."""
        if not self.current_image:
            return

        data = self.current_image.tobytes("raw", "RGB")
        
        # Create a QImage from the byte data and set the pixmap with it
        q_image = QImage(data, self.current_image.width, self.current_image.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(
            self.image_viewer.size(), 
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.image_viewer.pixmap = scaled_pixmap
        self.image_viewer.setPixmap(
            QPixmap.fromImage(q_image).scaled(
                self.image_viewer.size(), 
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )