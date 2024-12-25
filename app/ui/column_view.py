#column_view.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QMenu, QDialog, QMessageBox
from PySide6.QtCore import Qt
from app.ui.card_view import CardView
from assets.styles import Styles
from assets.dialogues.rename_card_dialogue import RenameCardDialog
from assets.dialogues.delete_card_dialogue import DeleteCardDialog

class ColumnView(QWidget):
    def __init__(self, list_column, app_manager, parent=None):
        super().__init__(parent)
        self.list_column = list_column
        self.app_manager = app_manager

        # Set column size constraints
        self.setFixedWidth(320)

        # Apply column styles
        self.setStyleSheet(Styles.column_style)

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        # Column header
        self.name_label = QLabel(list_column.name)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet(Styles.column_title_style)
        self.name_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.name_label.customContextMenuRequested.connect(self.show_context_menu)
        self.layout.addWidget(self.name_label)

        # Scrollable area for cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setFixedWidth(300)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignTop)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)

        # Disable horizontal scrolling
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.card_container = QWidget()
        self.card_layout = QVBoxLayout()
        self.card_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.card_layout.setContentsMargins(5, 0, 10, 0)
        self.card_container.setLayout(self.card_layout)
        self.card_container.setFixedWidth(300)
        self.scroll_area.setWidget(self.card_container)
        self.layout.addWidget(self.scroll_area)

        self.setAcceptDrops(True)

        # Cards in the column
        for card in self.list_column.cards:
            card_view = CardView(card, self.app_manager, self)
            self.card_layout.addWidget(card_view)

        # Add Card Button
        self.add_card_button_container = QWidget()
        self.card_container.setFixedWidth(300)
        self.add_card_button_layout = QVBoxLayout()
        self.add_card_button_layout.setContentsMargins(10, 0, 0, 0)
        self.add_card_button_layout.setAlignment(Qt.AlignHCenter)
        self.add_card_button_container.setLayout(self.add_card_button_layout)

        self.add_card_button = QPushButton("Add Card")
        self.add_card_button.setStyleSheet(Styles.add_card_button_style)
        self.add_card_button.setFixedSize(100, 30)
        self.add_card_button.clicked.connect(self.add_card)
        self.add_card_button_layout.addWidget(self.add_card_button)

        # Add the button container to the card layout
        self.card_layout.addWidget(self.add_card_button_container)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        """
        Tracks the drag position within the column to reorder cards.
        """
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        Handles dropping a card into this column.
        """
        card_name = event.mimeData().text()

        # Find the source column
        source_column = self.app_manager.get_column_containing_card(card_name)
        if not source_column:
            event.ignore()
            return

        # If the source column is the same as the destination column, do nothing
        if source_column == self.list_column:
            event.ignore()
            return

        # Remove the card from the source column
        card = next((c for c in source_column.cards if c.name == card_name), None)
        if card:
            source_column.cards.remove(card)
            source_column_view = self._get_column_view(source_column)
            if source_column_view:
                source_column_view._remove_card_from_column_ui(card_name)

            # Add the card to this column
            self.list_column.cards.append(card)
            self._add_card_to_column_ui(card)

            # Save state and refresh the UI
            self.app_manager.save_state()

        event.acceptProposedAction()

    def _reorder_column_ui(self):
        # Remove all cards from the layout
        while self.card_layout.count() > 1:
            item = self.card_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Re-add cards in the new order
        for card in self.list_column.cards:
            self._add_card_to_column_ui(card)

    def _remove_card_from_column_ui(self, card_name):
        for i in range(self.card_layout.count()):
            widget = self.card_layout.itemAt(i).widget()
            if isinstance(widget, CardView) and widget.card.name == card_name:
                widget.deleteLater()
                break

    def _add_card_to_column_ui(self, card):
        card_view = CardView(card, self.app_manager, self)
        self.card_layout.insertWidget(self.card_layout.count() - 1, card_view)

    def _get_column_view(self, list_column):
        for i in range(self.app_manager.main_window.board_view.content_layout.count()):
            widget = self.app_manager.main_window.board_view.content_layout.itemAt(i).widget()
            if isinstance(widget, ColumnView) and widget.list_column == list_column:
                return widget
        return None

    def add_card(self):
        dialog = RenameCardDialog("", parent=self, dialog_title="Add Card")
        dialog.setStyleSheet(Styles.dialog_style)
        if dialog.exec() == QDialog.Accepted:
            card_name = dialog.get_new_name().strip()
            if not card_name:
                QMessageBox.warning(self, "Invalid Name", "Card name cannot be empty.")
                return

            new_card = self.list_column.add_card(card_name)
            self._add_card_to_column_ui(new_card)

            self.add_card_button_layout.setAlignment(Qt.AlignHCenter)

            self.app_manager.save_state()

    def show_context_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet(Styles.context_menu_style)
        rename_action = menu.addAction("Rename Column")
        delete_action = menu.addAction("Delete Column")

        action = menu.exec(self.name_label.mapToGlobal(pos))
        if action == rename_action:
            self.rename_column()
        elif action == delete_action:
            self.delete_column()

    def rename_column(self):
        dialog = RenameCardDialog(self.list_column.name, self)
        dialog.setStyleSheet(Styles.dialog_style)
        if dialog.exec() == QDialog.Accepted:
            new_name = dialog.get_new_name()
            if new_name:
                self.list_column.name = new_name
                self.name_label.setText(new_name)
                self.app_manager.save_state()

    def delete_column(self):
        dialog = DeleteCardDialog(self.list_column.name, self)
        dialog.setStyleSheet(Styles.dialog_style)
        if dialog.exec() == QDialog.Accepted:
            self.app_manager.remove_column_from_board(self.list_column)
            self.recursive_delete()
            self.app_manager.save_state()
            self.deleteLater()

    def recursive_delete(self):
        for card in self.list_column.cards:
            self.recursive_delete_card(card)
        self.list_column.cards.clear()

    def recursive_delete_card(self, card):
        if card.board:
            for list_column in card.board.lists:
                for nested_card in list_column.cards:
                    self.recursive_delete_card(nested_card)
        card.board = None