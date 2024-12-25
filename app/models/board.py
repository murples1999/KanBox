#board.py

class Board:
    def __init__(self, name, lists=None):
        self.name = name
        self.lists = lists or []
        self.description = ""

    def to_dict(self):
        return {
            "name": self.name,
            "lists": [list_column.to_dict() for list_column in self.lists],
            "description": self.description,  # Include the description
        }
    
    @staticmethod
    def from_dict(data):
        from app.models.list_column import ListColumn
        board = Board(
            name=data["name"],
            lists=[ListColumn.from_dict(l) for l in data["lists"]],
        )
        board.description = data.get("description", "")  # Restore the description
        return board

    def add_list(self, list_name):
        from app.models.list_column import ListColumn
        new_list = ListColumn(list_name)
        self.lists.append(new_list)