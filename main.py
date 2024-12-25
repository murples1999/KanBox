# main.py
import sys
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow

def main():
    # Create the Qt application
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Execute the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()