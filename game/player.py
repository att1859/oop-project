from game.field import FIELD_FULL_MESSAGE, Field


MAX_HAND_SIZE = 5
TURN_DRAW_COUNT = 2
STARTING_HAND_SIZE = MAX_HAND_SIZE - TURN_DRAW_COUNT


class Player:
    def __init__(self, name, health=30, mana=10, deck=None):
        self.name = name
        self.health = health
        self.max_mana = mana
        self.mana = mana
        self.deck = deck if deck is not None else []
        self.hand = []
        # 플레이어별로 필드를 가짐
        self.field = Field()
        self.draw_starting_hand()

    def take_damage(self, amount):
        self.health -= amount

    def is_defeated(self):
        return self.health <= 0

    def can_play(self, card):
        # 카드 비용 검사는 Player가 담당
        return self.mana >= card.cost

    def refresh_mana(self):
        # 최소 버전: 턴마다 마나를 최대치로 회복
        self.mana = self.max_mana

    def draw_starting_hand(self):
        for _ in range(STARTING_HAND_SIZE):
            self.draw_card()

    def draw_card(self):
        if len(self.hand) >= MAX_HAND_SIZE:
            return [f"{self.name}'s hand is full."]

        if not self.deck:
            return [f"{self.name}'s deck is empty."]

        card = self.deck.pop(0)
        self.hand.append(card)
        return [f"{self.name} drew {card.name}."]

    def draw_cards(self, count):
        messages = []
        for _ in range(count):
            messages += self.draw_card()
        return messages

    def start_turn(self):
        self.refresh_mana()
        for minion in self.field.minions:
            minion.has_attacked = False

        return self.draw_cards(TURN_DRAW_COUNT)

    def play_card(self, card_index, opponent):
        if card_index < 0 or card_index >= len(self.hand):
            return False, ["Invalid card number."]

        card = self.hand[card_index]

        if not self.can_play(card):
            return False, [f"Not enough mana to play {card.name}."]

        self.mana -= card.cost
        messages = card.play(self, opponent)

        if messages == [FIELD_FULL_MESSAGE]:
            self.mana += card.cost
            return False, messages

        # 사용한 카드는 손패에서 제거
        self.hand.pop(card_index)
        return True, messages
