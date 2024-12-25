#rename_card_dialogue.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QPlainTextEdit, QHBoxLayout
from assets.styles import Styles
from PySide6.QtCore import Qt

class CustomPlainTextEdit(QPlainTextEdit):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setPlainText(text)

    def keyPressEvent(self, event):
        if event.key() in {Qt.Key_Return, Qt.Key_Enter}:
            if event.modifiers() & Qt.ShiftModifier:
                cursor = self.textCursor()
                cursor.insertText("\n")
            else:
                self.parent().accept()
        else:
            super().keyPressEvent(event)


class RenameCardDialog(QDialog):
    def __init__(self, current_name="", parent=None, dialog_title="Rename Card"):
        super().__init__(parent)
        self.setWindowTitle(dialog_title)
        self.setStyleSheet(Styles.dialog_style)
        self.setMinimumSize(300, 150)

        # Layout
        self.layout = QVBoxLayout(self)

        # Instruction Label
        self.label = QLabel("Enter the new name for the card:")
        self.layout.addWidget(self.label)

        # Text Box
        self.name_input = CustomPlainTextEdit(current_name, self)
        self.layout.addWidget(self.name_input)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.rename_button = QPushButton("OK")
        self.rename_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.rename_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)

        # Focus on the text input
        self.name_input.setFocus()

    def get_new_name(self):
        return self.name_input.toPlainText().strip()