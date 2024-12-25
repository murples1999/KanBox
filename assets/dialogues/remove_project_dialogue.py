#remove_project_dialogue.py

from PySide6.QtWidgets import QVBoxLayout, QPushButton, QDialog, QLabel
from PySide6.QtCore import Qt
from assets.styles import Styles

class RemoveProjectDialog(QDialog):
    def __init__(self, project_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Remove Project")
        self.setFixedSize(300, 150)
        self.setStyleSheet(Styles.dialog_style)

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Message
        self.message_label = QLabel(f"Are you sure you want to delete the project '{project_name}'?")
        self.message_label.setWordWrap(True)
        self.layout.addWidget(self.message_label)

        # Buttons
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.accept)
        self.layout.addWidget(self.delete_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button)