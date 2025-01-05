from PyQt5.QtWidgets import QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(1000, 800)
        self.setText("Upload an Image")
        self.setObjectName("imageViewer")
        self.pixmap = None

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.pixmap = QPixmap(file_path)
            self.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio))

    def save_image(self):
        if self.pixmap:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
            if file_path:
                self.pixmap.save(file_path)


