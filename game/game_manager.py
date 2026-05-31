from game.card import MinionCard, SpellCard
from game.player import Player


class GameManager:
    # 게임 규칙 담당: 콘솔 입력/출력은 하지 않음
    def __init__(self):
        self.players = [
            Player("Player 1", hand=self._create_starting_hand()),
            Player("Player 2", hand=self._create_starting_hand()),
        ]
        self.current_player_index = 0

    def _create_starting_hand(self):
        # 최소 버전: cards.json 대신 코드에서 직접 카드를 만듦
        return [
            MinionCard("River Crocolisk", 2, "A simple minion.", 2, 3),
            MinionCard("Boulderfist Ogre", 6, "A strong minion.", 6, 7),
            SpellCard("Fireball", 4, "Deal 6 damage.", 6),
            SpellCard("Arcane Shot", 1, "Deal 2 damage.", 2),
        ]

    def get_current_player(self):
        return self.players[self.current_player_index]

    def get_opponent(self):
        return self.players[1 - self.current_player_index]

    def play_card(self, card_index):
        current_player = self.get_current_player()
        opponent = self.get_opponent()

        # UI의 1번 카드 선택은 ConsoleUI에서 0번 인덱스로 바꿈
        if card_index < 0 or card_index >= len(current_player.hand):
            return False, "Invalid card number."

        return current_player.play_card(card_index, opponent)

    def end_turn(self):
        # 턴 전환 후 새 현재 플레이어의 마나를 회복
        self.current_player_index = 1 - self.current_player_index
        self.get_current_player().refresh_mana()

    def get_winner(self):
        for player in self.players:
            if player.is_defeated():
                return self.players[1 - self.players.index(player)]
        return None

    def is_game_over(self):
        return self.get_winner() is not None
