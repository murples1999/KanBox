#card.py

class Card:
    def __init__(self, name):
        self.name = name
        self.board = None

    def to_dict(self):
        return {
            "name": self.name,
            "board": self.board.to_dict() if self.board else None,
        }
    
    @staticmethod
    def from_dict(data):
        from app.models.board import Board  # Lazy import
        card = Card(data["name"])
        card.board = Board.from_dict(data["board"]) if data["board"] else None
        return card