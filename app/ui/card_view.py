#card_view.py

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QMenu, QDialog, QSizePolicy
from PySide6.QtCore import Qt, QMimeData, QTimer
from PySide6.QtGui import QDrag
from assets.styles import Styles
from assets.dialogues.rename_card_dialogue import RenameCardDialog
from assets.dialogues.delete_card_dialogue import DeleteCardDialog

class CardView(QWidget):
    def __init__(self, card, app_manager, column_view, parent=None):
        super().__init__(parent)
        self.card = card
        self.app_manager = app_manager
        self.column_view = column_view

        # Fix the card width
        self.setFixedWidth(300)

        # Apply card styles
        self.setStyleSheet(Styles.card_style)

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(self.layout)

        # Card name
        self.name_label = QLabel(card.name)
        self.name_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.name_label.setWordWrap(True)
        self.name_label.setFixedWidth(280)
        self.name_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.layout.addWidget(self.name_label)

        # Dynamically adjust height
        self.adjust_card_height()

        self.setCursor(Qt.PointingHandCursor)

        # Long press detection
        self.long_press_timer = QTimer()
        self.long_press_timer.setInterval(500)
        self.long_press_timer.timeout.connect(self.start_drag)

        self.mouse_pressed_pos = None

    def adjust_card_height(self):
        self.name_label.adjustSize()
        content_height = self.name_label.sizeHint().height()
        total_height = (
            content_height
            + self.layout.contentsMargins().top()
            + self.layout.contentsMargins().bottom()
        )
        self.setFixedHeight(total_height)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed_pos = event.pos()
            self.long_press_timer.start()
        elif event.button() == Qt.RightButton:
            self.show_context_menu(event)

    def mouseReleaseEvent(self, event):
        self.long_press_timer.stop()
        if event.button() == Qt.LeftButton and self.mouse_pressed_pos is not None:
            if (event.pos() - self.mouse_pressed_pos).manhattanLength() < 10:
                self.handle_left_click()

    def start_drag(self):
        self.long_press_timer.stop()

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.card.name)
        drag.setMimeData(mime_data)
        drag.exec(Qt.MoveAction)

    def handle_left_click(self):
        if not self.card.board:
            self.card.board = self.app_manager.create_board(f"Board for {self.card.name}")
        self.app_manager.navigate_to_card(self.card)

    def show_context_menu(self, event):
        menu = QMenu(self)
        menu.setStyleSheet(Styles.context_menu_style)

        move_up_action = menu.addAction("Move Up")
        move_down_action = menu.addAction("Move Down")
        move_to_top_action = menu.addAction("Move to Top")
        move_to_bottom_action = menu.addAction("Move to Bottom")

        rename_action = menu.addAction("Rename")
        delete_action = menu.addAction("Delete")

        action = menu.exec(event.globalPos())

        if action == move_up_action:
            self.move_card(-1)
        elif action == move_down_action:
            self.move_card(1)
        elif action == move_to_top_action:
            self.move_card_to_position(0)
        elif action == move_to_bottom_action:
            self.move_card_to_position(len(self.column_view.list_column.cards) - 1)
        elif action == rename_action:
            self.rename_card()
        elif action == delete_action:
            self.delete_card()

    def move_card(self, offset):
        column = self.column_view.list_column
        index = column.cards.index(self.card)
        new_index = index + offset

        if 0 <= new_index < len(column.cards):
            column.cards.insert(new_index, column.cards.pop(index))
            self.column_view._reorder_column_ui()
            self.app_manager.save_state()

    def move_card_to_position(self, position):
        column = self.column_view.list_column
        index = column.cards.index(self.card)

        if 0 <= position < len(column.cards) and position != index:
            column.cards.insert(position, column.cards.pop(index))
            self.column_view._reorder_column_ui()
            self.app_manager.save_state()

    def rename_card(self):
        dialog = RenameCardDialog(self.card.name, parent=self, dialog_title="Rename Card")
        dialog.setStyleSheet(Styles.dialog_style)
        if dialog.exec() == QDialog.Accepted:
            new_name = dialog.get_new_name()
            if new_name:
                self.card.name = new_name
                self.name_label.setText(new_name)
                self.adjust_card_height()
                self.app_manager.save_state()

    def delete_card(self):
        dialog = DeleteCardDialog(self.card.name, self)
        dialog.setStyleSheet(Styles.dialog_style)
        if dialog.exec() == QDialog.Accepted:
            self.recursive_delete(self.card)
            self.app_manager.save_state()
            self.deleteLater()

    def recursive_delete(self, card):
        if card.board:
            for list_column in card.board.lists:
                for nested_card in list_column.cards:
                    self.recursive_delete(nested_card)
        card.board = None
        self.app_manager.remove_card_from_board(card)