#board_view.py

from functools import partial
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QPushButton, QMessageBox, 
                               QHBoxLayout, QLabel, QSizePolicy, QPlainTextEdit)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QTextOption, QShortcut, QKeySequence
from app.ui.column_view import ColumnView
from app.models.list_column import ListColumn
from assets.styles import Styles

class BoardView(QWidget):
    def __init__(self, parent=None, app_manager=None):
        super().__init__(parent)
        self.app_manager = app_manager

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        # Top bar layout
        self.top_bar_layout = QHBoxLayout()
        self.top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(self.top_bar_layout)

        # Board title
        self.board_title = QLabel("Board Title")
        self.board_title.setAlignment(Qt.AlignCenter)
        self.board_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.board_title.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.top_bar_layout.addWidget(self.board_title)

        # Back button
        self.back_button = QPushButton("<-")
        self.back_button.setFixedSize(40, 30)
        self.back_button.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.back_button.clicked.connect(self.navigate_back)
        self.top_bar_layout.addWidget(self.back_button)

        # Description area
        self.board_description = QPlainTextEdit(self)
        self.board_description.setPlaceholderText("Enter a description for this board...")
        self.board_description.setStyleSheet("""
            QPlainTextEdit {
                background-color: transparent;
                border: none;
                font-size: 14px;
                color: white;
            }
        """)
        self.board_description.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.board_description.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.board_description.textChanged.connect(self.adjust_description_height)
        self.board_description.focusOutEvent = self.save_description
        self.layout.addWidget(self.board_description)

        # Scrollable area
        self.scroll_area = QScrollArea()
        self.scroll_area.setContentsMargins(1 , 1, 1, 1)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet(Styles.board_style)
        self.layout.addWidget(self.scroll_area)

        # Container for board content
        self.content_widget = QWidget()
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(1, 1, 1, 1)
        self.content_layout.setSpacing(1)
        self.content_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.content_widget.setLayout(self.content_layout)
        self.scroll_area.setWidget(self.content_widget)

        # Breadcrumbs container
        self.breadcrumb_container = QWidget()
        self.breadcrumb_layout = QHBoxLayout()
        self.breadcrumb_layout.setContentsMargins(0, 0, 0, 0)
        self.breadcrumb_layout.setSpacing(5)
        self.breadcrumb_layout.setAlignment(Qt.AlignCenter)
        self.breadcrumb_container.setLayout(self.breadcrumb_layout)
        self.layout.addWidget(self.breadcrumb_container)

        # Add Column button wrapper
        self.button_wrapper = QWidget()
        self.button_wrapper_layout = QVBoxLayout()
        self.button_wrapper_layout.setContentsMargins(0, 10, 0, 0)
        self.button_wrapper_layout.setAlignment(Qt.AlignTop)
        self.button_wrapper.setLayout(self.button_wrapper_layout)

        self.add_column_button = QPushButton("Add Column")
        self.add_column_button.setFixedSize(150, 30)
        self.add_column_button.setStyleSheet(Styles.add_column_button_style)
        self.add_column_button.clicked.connect(self.add_column)
        self.button_wrapper_layout.addWidget(self.add_column_button)

        # Hotkey: Left Arrow -> Back Button
        self.back_shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.back_shortcut.activated.connect(self.navigate_back)

    def adjust_description_height(self):
        document_height = self.board_description.document().size().height()
        padding = 15
        total_height = max(50, int(document_height + padding))
        
        self.board_description.setFixedHeight(total_height)

    def save_description(self, event):
        if self.board:
            self.board.description = self.board_description.toPlainText().strip()
            self.app_manager.save_state()
        QPlainTextEdit.focusOutEvent(self.board_description, event)

    def update_breadcrumbs(self):
        while self.breadcrumb_layout.count():
            widget = self.breadcrumb_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        MAX_BREADCRUMB_LENGTH = 20

        stack = self.app_manager.navigation_manager.get_navigation_stack()
        for i, node in enumerate(stack):
            breadcrumb_name = node.name.replace("Board for ", "")
            if len(breadcrumb_name) > MAX_BREADCRUMB_LENGTH:
                breadcrumb_name = breadcrumb_name[:MAX_BREADCRUMB_LENGTH - 3] + "..."
            breadcrumb_button = QPushButton(breadcrumb_name)
            breadcrumb_button.setStyleSheet(Styles.breadcrumb_button_style)
            breadcrumb_button.setCursor(Qt.PointingHandCursor)
            breadcrumb_button.clicked.connect(partial(self.navigate_to_breadcrumb, i))
            self.breadcrumb_layout.addWidget(breadcrumb_button)

            if i < len(stack) - 1:
                separator = QLabel("/")
                self.breadcrumb_layout.addWidget(separator)

    def navigate_to_breadcrumb(self, index):
        target_board = self.app_manager.navigation_manager.navigate_to_index(index)
        self.display_board(target_board)

    def navigate_back(self):
        previous_board = self.app_manager.go_back()
        if previous_board:
            self.display_board(previous_board)

    def display_board(self, board):
        self.board = board

        board_name = board.name.replace("Board for ", "")

        MAX_TITLE_LENGTH = 100

        if len(board_name) > MAX_TITLE_LENGTH:
            board_name = board_name[:MAX_TITLE_LENGTH - 3] + "..."

        self.board_title.setText(board_name)

        self.board_description.setPlainText(getattr(board, "description", ""))
        self.adjust_description_height()

        while self.content_layout.count():
            widget = self.content_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        for list_column in board.lists:
            column_view = ColumnView(list_column, parent=self, app_manager=self.app_manager)
            self.content_layout.addWidget(column_view)

        self.create_button_wrapper()

        self.content_layout.addWidget(self.button_wrapper, alignment=Qt.AlignTop)

        self.update_breadcrumbs()

    def create_button_wrapper(self):
        self.button_wrapper = QWidget()
        button_wrapper_layout = QVBoxLayout()
        button_wrapper_layout.setContentsMargins(0, 10, 0, 0)
        button_wrapper_layout.setAlignment(Qt.AlignTop)
        self.button_wrapper.setLayout(button_wrapper_layout)

        self.add_column_button = QPushButton("Add Column")
        self.add_column_button.setFixedSize(150, 30)
        self.add_column_button.setStyleSheet(Styles.add_column_button_style)
        self.add_column_button.clicked.connect(self.add_column)
        button_wrapper_layout.addWidget(self.add_column_button)

    def add_column(self):
        if not hasattr(self, "board") or self.board is None:
            QMessageBox.warning(self, "No Board", "No board is loaded to add a column.")
            return

        new_column_name = f"New Column {len(self.board.lists) + 1}"
        new_column = ListColumn(new_column_name)
        self.board.lists.append(new_column)

        self.add_list_to_board(new_column)
        self.app_manager.save_state()

        if self.content_layout.indexOf(self.button_wrapper) == -1:
            self.content_layout.addWidget(self.button_wrapper)

        self.scroll_to_right()

    def scroll_to_right(self):
        QTimer.singleShot(0, lambda: self.scroll_area.horizontalScrollBar().setValue(self.scroll_area.horizontalScrollBar().maximum()))

    def add_list_to_board(self, list_column):
        column_view = ColumnView(list_column, parent=self, app_manager=self.app_manager)
        self.content_layout.insertWidget(self.content_layout.count() - 1, column_view)

    def remove_list_from_board(self, list_column_name):
        for i in range(self.content_layout.count()):
            widget = self.content_layout.itemAt(i).widget()
            if isinstance(widget, ColumnView) and widget.list_column.name == list_column_name:
                widget.deleteLater()
                break

        self.app_manager.save_state()