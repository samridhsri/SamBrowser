import sys
from PyQt6.QtWidgets import QApplication
from main_window import StudyNavigator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudyNavigator()
    window.show()
    sys.exit(app.exec())