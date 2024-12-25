#app_manager.py

import os
from app.core.navigation_manager import NavigationManager
from app.models.project import Project
from app.models.board import Board
from app.core.state_manager import StateManager

class AppManager:
    def __init__(self, main_window=None):
        self.main_window = main_window
        self.navigation_manager = NavigationManager()
        self.projects = {}
        self.current_project = None
        self.last_open_project = None
        self.state_manager = StateManager()

    def set_project(self, project):
        self.current_project = project
        self.last_open_project = project.name if project else None
        self.navigation_manager = NavigationManager()
        if project and project.root_board:
            self.navigation_manager.navigate_to(project.root_board)

    def create_project(self, project_name):
        project = Project(name=project_name)
        self.projects[project_name] = project
        self.state_manager.add_project(project)
        self.save_state()
        return project

    def delete_project(self, project_name):
        if project_name in self.projects:
            del self.projects[project_name]
            self.state_manager.remove_project(project_name)
            if self.current_project and self.current_project.name == project_name:
                self.set_project(None)
            self.save_state()
        else:
            print(f"AppManager: Project '{project_name}' not found.")

    def load_state(self):
        """Loads the state from StateManager and initializes projects."""
        self.state_manager.load()
        self.projects = {project.name: project for project in self.state_manager.projects}
        self.last_open_project = self.state_manager.last_open_project

        if self.last_open_project and self.last_open_project in self.projects:
            self.set_project(self.projects[self.last_open_project])
            if self.main_window:
                self.main_window.sidebar.select_project(self.last_open_project)
                self.main_window.board_view.display_board(self.projects[self.last_open_project].root_board)
        else:
            self.set_project(None)
            if self.main_window:
                self.main_window.board_view.hide()

    def save_state(self):
        self.state_manager.last_open_project = self.last_open_project
        self.state_manager.save()

    def select_project(self, project_name):
        project = self.projects.get(project_name)
        if project:
            self.set_project(project)
        return project

    def navigate_to_card(self, card):
        if not card.board:
            card.board = self.create_board(f"Board for {card.name}")
            self.save_state()
        self.navigation_manager.navigate_to(card.board)
        self.refresh_board_view()

    def go_back(self):
        return self.navigation_manager.go_back()

    def get_current_board(self):
        return self.navigation_manager.get_current_board()
    
    def create_board(self, board_name):
        new_board = Board(board_name)
        self.save_state()
        return new_board
    
    def refresh_board_view(self):
        if self.main_window and self.main_window.board_view:
            current_board = self.navigation_manager.get_current_board()
            if current_board:
                self.main_window.board_view.display_board(current_board)

    def remove_card_from_board(self, card):
        current_board = self.navigation_manager.get_current_board()
        if current_board:
            for list_column in current_board.lists:
                if card in list_column.cards:
                    list_column.cards.remove(card)
                    break

    def remove_column_from_board(self, list_column):
        if self.current_project and self.current_project.root_board:
            self.current_project.root_board.lists = [
                column for column in self.current_project.root_board.lists if column != list_column
            ]

    def get_column_containing_card(self, card_name):
        current_board = self.get_current_board()
        if current_board:
            for column in current_board.lists:
                for card in column.cards:
                    if card.name == card_name:
                        return column
        return None