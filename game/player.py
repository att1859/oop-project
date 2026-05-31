class Player:
    def __init__(self, name, health=30, mana=10, hand=None):
        self.name = name
        self.health = health
        self.max_mana = mana
        self.mana = mana
        # 플레이어가 자신의 손패 상태 보유
        self.hand = hand if hand is not None else []

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

    def play_card(self, card_index, opponent):
        card = self.hand[card_index]

        if not self.can_play(card):
            return False, f"Not enough mana to play {card.name}."

        self.mana -= card.cost
        # 사용한 카드는 손패에서 제거
        self.hand.pop(card_index)
        return True, card.play(self, opponent)
