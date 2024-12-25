#sidebar.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QHBoxLayout, QMessageBox, QDialog
)
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtCore import Qt
from assets.dialogues.remove_project_dialogue import RemoveProjectDialog
from assets.dialogues.add_project_dialogue import AddProjectDialog
from assets.styles import Styles


class Sidebar(QWidget):
    def __init__(self, main_window=None):
        super().__init__(main_window)
        self.main_window = main_window
        self.collapsed = False

        # Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        # Header
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignTop)
        self.header = QLabel("Projects")
        self.collapse_button = QPushButton("<")
        self.collapse_button.setFixedSize(25, 25)
        self.collapse_button.clicked.connect(self.toggle_collapse)
        header_layout.addWidget(self.header)
        header_layout.addWidget(self.collapse_button)
        self.main_layout.addLayout(header_layout)

        # Project list
        self.project_list = QListWidget()
        self.main_layout.addWidget(self.project_list)

        # Project management buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add")
        self.add_button.setStyleSheet(Styles.project_button_style)
        self.remove_button = QPushButton("Remove")
        self.remove_button.setStyleSheet(Styles.project_button_style)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        self.main_layout.addLayout(button_layout)

        # Connect signals for buttons
        self.add_button.clicked.connect(self.add_project)
        self.remove_button.clicked.connect(self.remove_project)

        # Hotkey: CMD + N -> Add Project Button
        self.add_project_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self.add_project_shortcut.activated.connect(self.add_project)

    def toggle_collapse(self):
        self.collapsed = not self.collapsed

        self.project_list.setVisible(not self.collapsed)
        self.add_button.setVisible(not self.collapsed)
        self.remove_button.setVisible(not self.collapsed)
        self.header.setVisible(not self.collapsed)

        if self.collapsed:
            self.collapse_button.setText(">")
        else:
            self.collapse_button.setText("<")

    def add_project(self):
        dialog = AddProjectDialog(self)
        if dialog.exec() == QDialog.Accepted:
            project_name = dialog.get_project_name()
            if not project_name:
                QMessageBox.warning(self, "Invalid Input", "Project name cannot be empty.")
                return

            for index in range(self.project_list.count()):
                if self.project_list.item(index).text() == project_name:
                    QMessageBox.warning(self, "Duplicate Project", "A project with this name already exists.")
                    return

            if self.main_window:
                self.main_window.on_add_project(project_name=project_name)
                self.main_window.app_manager.save_state()

    def remove_project(self):
        selected_item = self.project_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "No Selection", "Please select a project to remove.")
            return

        project_name = selected_item.text()
        dialog = RemoveProjectDialog(project_name, self)

        if dialog.exec() == QDialog.Accepted:
            print(f"Sidebar: Removing project '{project_name}'")
            self.project_list.blockSignals(True)
            try:
                if self.main_window:
                    self.main_window.on_remove_project(project_name)
            finally:
                self.project_list.blockSignals(False)

    def update_project_list(self, projects):
        self.project_list.blockSignals(True)
        try:
            self.project_list.clear()
            self.project_list.addItems(projects)
        finally:
            self.project_list.blockSignals(False)

    def select_project(self, project_name):
        for i in range(self.project_list.count()):
            item = self.project_list.item(i)
            if item.text() == project_name:
                self.project_list.setCurrentRow(i)
                break

    def on_remove_project(self, project_name=None):
        self.sidebar.project_list.blockSignals(True)
        try:
            if not project_name:
                selected_item = self.sidebar.project_list.currentItem()
                if not selected_item:
                    QMessageBox.warning(self, "No Selection", "Please select a project to remove.")
                    return
                project_name = selected_item.text()

            current_index = self.sidebar.project_list.currentRow()
            self.app_manager.delete_project(project_name)
            self.sidebar.update_project_list(self.app_manager.projects.keys())

            if self.sidebar.project_list.count() > 0:
                next_index = current_index - 1 if current_index > 0 else 0
                self.sidebar.project_list.setCurrentRow(next_index)
                self.on_project_selected(self.sidebar.project_list.item(next_index))
            else:
                self.board_view.hide()
        finally:
            self.sidebar.project_list.blockSignals(False)