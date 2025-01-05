import sys
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QSlider, 
    QFrame, 
    QPushButton, 
    QLabel, 
    QGroupBox,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtCore, QtGui
from components.image_handler import ImageViewer
from components.adjustments import Adjustments
from components.history import History


class ImageAdjustmentTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Adjustment Tool")
        self.setGeometry(100, 100, 1000, 600)

        # Load stylesheet
        with open("ui/style.qss", "r") as file:
            self.setStyleSheet(file.read())

        # Components
        self.image_viewer = ImageViewer()
        self.history = History(self.image_viewer)
        self.adjustments = Adjustments(self.image_viewer, self.history)

        self.init_ui()


    def init_ui(self):
        # Main Layout
        main_layout = QHBoxLayout(self)


        # Image Viewer (3/4 of the window)
        main_layout.addWidget(self.image_viewer, 3)

        # Right Panel (1/4 of the window)
        right_panel = QVBoxLayout()
        right_container = QFrame()
        right_container.setLayout(right_panel)
        right_container.setObjectName("rightPanel")
        main_layout.addWidget(right_container, 1)

        # Sliders for Brightness, Contrast, Saturation, Sharpness, and Exposure
        
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(-100)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.sliderReleased.connect(
            lambda: self.adjustments.adjust_brightness(self.brightness_slider.value())
        )

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(0)
        self.contrast_slider.setMaximum(50)
        self.contrast_slider.setValue(10)
        self.contrast_slider.sliderReleased.connect(
            lambda: self.adjustments.adjust_contrast(self.contrast_slider.value())
        )

        self.saturation_slider = QSlider(Qt.Horizontal)
        self.saturation_slider.setMinimum(0)
        self.saturation_slider.setMaximum(50)
        self.saturation_slider.setValue(10)
        self.saturation_slider.sliderReleased.connect(
                lambda: self.adjustments.adjust_saturation(self.saturation_slider.value())
            )

        self.sharpness_slider = QSlider(Qt.Horizontal)
        self.sharpness_slider.setMinimum(-100)
        self.sharpness_slider.setMaximum(100)
        self.sharpness_slider.setValue(0)
        self.sharpness_slider.sliderReleased.connect(
                lambda: self.adjustments.adjust_sharpness(self.sharpness_slider.value())
            )

        self.exposure_slider = QSlider(Qt.Horizontal)
        self.exposure_slider.setMinimum(-100)
        self.exposure_slider.setMaximum(100)
        self.exposure_slider.setValue(0)
        self.exposure_slider.sliderReleased.connect(
                lambda: self.adjustments.adjust_exposure(self.exposure_slider.value())
            )

        # Buttons
        undo_button = QPushButton("Undo")
        undo_button.clicked.connect(self.history.undo)

        redo_button = QPushButton("Redo")
        redo_button.clicked.connect(self.history.redo)

        grayscale_filter_button = QPushButton("Grayscale")
        grayscale_filter_button.clicked.connect(self.adjustments.apply_grayscale_filter)

        sepia_filter_button = QPushButton("Sepia")
        sepia_filter_button.clicked.connect(self.adjustments.apply_sepia_filter)

        invert_filter_button = QPushButton("Invert")
        invert_filter_button.clicked.connect(self.adjustments.apply_invert_filter)

        cool_tone_filter_button = QPushButton("Cool Tone")
        cool_tone_filter_button.clicked.connect(self.adjustments.apply_cool_tone_filter)

        bright_glow_filter_button = QPushButton("Bright Glow")
        bright_glow_filter_button.clicked.connect(self.adjustments.apply_bright_glow_filter)

        # Upload and Save Buttons
        upload_button = QPushButton("Upload Image")
        upload_button.setObjectName("uploadButton")
        upload_button.clicked.connect(self.open_image)

        save_button = QPushButton("Save Image")
        save_button.setObjectName("saveButton")
        save_button.clicked.connect(self.image_viewer.save_image)


        # Adjustments Sliders
        slider_group = QGroupBox("Adjustments")
        slider_layout = QVBoxLayout()

        slider_layout.addWidget(QLabel("Brightness"))
        slider_layout.addWidget(self.brightness_slider)
        slider_layout.addWidget(QLabel("Contrast"))
        slider_layout.addWidget(self.contrast_slider)
        slider_layout.addWidget(QLabel("Saturation"))
        slider_layout.addWidget(self.saturation_slider)
        slider_layout.addWidget(QLabel("Sharpness"))
        slider_layout.addWidget(self.sharpness_slider)
        slider_layout.addWidget(QLabel("Exposure"))
        slider_layout.addWidget(self.exposure_slider)

        slider_group.setLayout(slider_layout)
        right_panel.addWidget(slider_group)

        # Spacer for aesthetics
        spacer = QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Fixed)
        right_panel.addItem(spacer)

        # Filter Buttons
        filter_group = QGroupBox("Filters")
        filter_layout = QHBoxLayout()

        filter_layout.addWidget(grayscale_filter_button)
        filter_layout.addWidget(sepia_filter_button)
        filter_layout.addWidget(invert_filter_button)
        filter_layout.addWidget(cool_tone_filter_button)
        filter_layout.addWidget(bright_glow_filter_button)

        filter_group.setLayout(filter_layout)
        right_panel.addWidget(filter_group)

        # Spacer for aesthetics
        right_panel.addStretch()

        # Bottom Buttons
        bottom_bar = QHBoxLayout()
        bottom_bar.addWidget(undo_button)
        bottom_bar.addWidget(redo_button)
        right_panel.addLayout(bottom_bar)

        # Upload Button
        right_panel.addWidget(upload_button)

        # Save Button
        right_panel.addWidget(save_button)
    
    def open_image(self):
        self.image_viewer.upload_image()
        self.adjustments.load_image()