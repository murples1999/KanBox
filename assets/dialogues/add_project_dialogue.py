#add_project_dialogue.py

from PySide6.QtWidgets import QVBoxLayout, QPushButton, QDialog, QLineEdit
from PySide6.QtCore import Qt
from assets.styles import Styles

class AddProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Project")
        self.setFixedSize(300, 150)
        self.setStyleSheet(Styles.dialog_style)

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Input
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter project name...")
        self.layout.addWidget(self.name_input)

        # Buttons
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.accept)
        self.layout.addWidget(self.add_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button)

    def get_project_name(self):
        return self.name_input.text().strip()