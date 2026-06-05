import random
from pathlib import Path

from game.card_loader import CardLoader
from game.player import Player


CARDS_FILE_PATH = Path(__file__).resolve().parent.parent / "data" / "cards.json"


class GameManager:
    # 게임 규칙 담당: 콘솔 입력/출력은 하지 않음
    def __init__(self):
        self.players = [
            Player("Player 1", deck=self._create_deck()),
            Player("Player 2", deck=self._create_deck()),
        ]
        self.current_player_index = 0
        self.start_turn_messages = self.start_turn()

    def _create_deck(self):
        deck = CardLoader(CARDS_FILE_PATH).load_cards()
        random.shuffle(deck)
        return deck

    def get_current_player(self):
        return self.players[self.current_player_index]

    def get_opponent(self):
        return self.players[1 - self.current_player_index]

    def play_card(self, card_index):
        current_player = self.get_current_player()
        opponent = self.get_opponent()

        success, messages = current_player.play_card(card_index, opponent)
        messages += self.cleanup_dead_minions()
        return success, messages

    def attack_minion(self, attacker_index, target_index):
        current_player = self.get_current_player()
        opponent = self.get_opponent()

        if attacker_index < 0 or attacker_index >= len(current_player.field.minions):
            return False, ["Invalid attacker number."]

        if target_index < 0 or target_index >= len(opponent.field.minions):
            return False, ["Invalid target number."]

        attacker = current_player.field.minions[attacker_index]
        target = opponent.field.minions[target_index]

        if attacker.has_attacked:
            return False, [f"{attacker.name} cannot attack this turn."]

        target.take_damage(attacker.attack)
        attacker.take_damage(target.attack)
        attacker.has_attacked = True

        messages = [
            f"{attacker.name} attacked {target.name}.",
            f"{target.name} took {attacker.attack} damage.",
            f"{attacker.name} took {target.attack} damage.",
        ]
        messages += self.cleanup_dead_minions()
        return True, messages

    def attack_hero(self, attacker_index):
        current_player = self.get_current_player()
        opponent = self.get_opponent()

        if attacker_index < 0 or attacker_index >= len(current_player.field.minions):
            return False, ["Invalid attacker number."]

        attacker = current_player.field.minions[attacker_index]
        if attacker.has_attacked:
            return False, [f"{attacker.name} cannot attack this turn."]

        opponent.take_damage(attacker.attack)
        attacker.has_attacked = True

        messages = [
            f"{attacker.name} attacked {opponent.name}.",
            f"{opponent.name} took {attacker.attack} damage.",
        ]
        messages += self.cleanup_dead_minions()
        return True, messages

    def attack_target(self, attacker_index, target_choice):
        opponent = self.get_opponent()

        if target_choice == 0:
            return self.attack_hero(attacker_index)

        target_index = target_choice - 1
        if target_index < 0 or target_index >= len(opponent.field.minions):
            return False, ["Invalid target number."]

        return self.attack_minion(attacker_index, target_index)

    def cleanup_dead_minions(self):
        messages = []
        for player in self.players:
            messages += player.field.remove_dead_minions()
        return messages

    def start_turn(self):
        return self.get_current_player().start_turn()

    def end_turn(self):
        self.current_player_index = 1 - self.current_player_index
        return self.start_turn()

    def get_winner(self):
        for player in self.players:
            if player.is_defeated():
                return self.players[1 - self.players.index(player)]
        return None

    def is_game_over(self):
        return self.get_winner() is not None
