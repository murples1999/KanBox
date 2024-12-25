#main_window.py

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt
from app.ui.sidebar import Sidebar
from app.ui.board_view import BoardView
from app.core.app_manager import AppManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KanBox")
        self.resize(800, 600)

        # Initialize App Manager before BoardView
        self.app_manager = AppManager(main_window=self)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layouts
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        # Sidebar
        self.sidebar = Sidebar(main_window=self)
        self.sidebar.setMaximumWidth(300)
        main_layout.addWidget(self.sidebar)

        # Main board area
        self.board_view = BoardView(app_manager=self.app_manager)
        main_layout.addWidget(self.board_view, stretch=0)

        # Load all projects on startup
        self.app_manager.load_state()
        self.sidebar.update_project_list(self.app_manager.projects.keys())

        # Connect signals
        self.sidebar.project_list.itemClicked.connect(self.on_project_selected)
        self.sidebar.remove_button.clicked.connect(self.on_remove_project)

    def on_project_selected(self, item):
        if not item:
            self.board_view.hide()
            return

        project_name = item.text()
        project = self.app_manager.select_project(project_name)

        if project:
            self.app_manager.last_open_project = project_name
            self.app_manager.save_state()

            if project.root_board:
                self.board_view.show()
                self.board_view.display_board(project.root_board)
            else:
                QMessageBox.warning(self, "No Board", "The selected project does not have a valid board.")

    def on_add_project(self, project_name=None):
        new_project = self.app_manager.create_project(project_name)
        self.sidebar.update_project_list([p.name for p in self.app_manager.state_manager.projects])
        self.sidebar.select_project(new_project.name)
        self.on_project_selected(self.sidebar.project_list.findItems(new_project.name, Qt.MatchExactly)[0])

    def on_remove_project(self, project_name=None):
        if project_name:
            self.app_manager.delete_project(project_name)
            self.sidebar.update_project_list(self.app_manager.projects.keys())
            self.app_manager.set_project(None)
            self.board_view.hide()