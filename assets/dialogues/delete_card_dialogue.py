#delete_card_dialogue.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class DeleteCardDialog(QDialog):
    def __init__(self, card_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Card")
        self.setFixedSize(300, 150)

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Message
        self.label = QLabel(f"Are you sure you want to delete '{card_name}' and all its contents?")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Buttons
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.accept)
        self.layout.addWidget(self.delete_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button)