#project.py

from app.models.board import Board

class Project:
    def __init__(self, name, root_board=None):
        self.name = name
        self.root_board = root_board or Board(name)

    def rename(self, new_name):
        self.name = new_name

    def to_dict(self):
        return {
            "name": self.name,
            "root_board": self.root_board.to_dict() if self.root_board else None,
        }

    @staticmethod
    def from_dict(data):
        return Project(
            name=data["name"],
            root_board=Board.from_dict(data["root_board"]) if data.get("root_board") else None,
        )