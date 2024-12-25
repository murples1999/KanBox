#list_column.py

class ListColumn:
    def __init__(self, name, cards=None):
        self.name = name
        self.cards = cards or []

    def add_card(self, card_name):
        from app.models.card import Card
        if not card_name:
            raise ValueError("Card name cannot be empty.")
        new_card = Card(name=card_name)
        self.cards.append(new_card)
        return new_card

    def to_dict(self):
        return {
            "name": self.name,
            "cards": [card.to_dict() for card in self.cards],
        }

    @staticmethod
    def from_dict(data):
        from app.models.card import Card
        return ListColumn(
            name=data["name"],
            cards=[Card.from_dict(card) for card in data["cards"]]
        )