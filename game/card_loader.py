import json
from pathlib import Path

from game.card import MinionCard, SpellCard


class CardLoader:
    def __init__(self, source: Path):
        self.source = source

    def data_iter(self):
        with self.source.open(encoding="utf-8") as source_file:
            card_data_list = json.load(source_file)

        yield from card_data_list

    def load_cards(self):
        return [self._create_card(card_data) for card_data in self.data_iter()]

    def _create_card(self, card_data):
        card_type = card_data["type"]

        if card_type == "minion":
            return MinionCard(
                card_data["name"],
                card_data["cost"],
                card_data["description"],
                card_data["attack"],
                card_data["health"],
            )

        if card_type == "spell":
            return SpellCard(
                card_data["name"],
                card_data["cost"],
                card_data["description"],
                card_data["damage"],
            )

        raise ValueError(f"Unknown card type: {card_type}")