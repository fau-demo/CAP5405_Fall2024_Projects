import sys

from PyQt5.QtWidgets import QApplication
from ui.main_window import ImageAdjustmentTool

def load_stylesheet(file_path):
    """Load the QSS file for styling."""
    with open(file_path, "r") as file:
        return file.read()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    stylesheet = load_stylesheet("ui/style.qss")
    app.setStyleSheet(stylesheet)

    window = ImageAdjustmentTool()
    window.show()
    sys.exit(app.exec_())
