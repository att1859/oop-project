from abc import ABC, abstractmethod


class Card(ABC):
    # 모든 카드가 공유하는 부모 클래스
    def __init__(self, name : str, cost : int, description : str):
        self.name = name
        self.cost = cost
        self.description = description

    @abstractmethod
    def play(self, owner, opponent):
        pass

    def __str__(self):
        return f"{self.name} (Cost: {self.cost}) - {self.description}"
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, cost={self.cost})"


class MinionCard(Card):
    # Card를 상속받아 하수인 전용 속성 추가
    def __init__(self, name, cost, description, attack, health):
        super().__init__(name, cost, description)
        self.attack = attack
        self.health = health

    def play(self, owner, opponent):
        # 최소 버전: 하수인은 필드에 남지 않고 즉시 피해 적용
        opponent.take_damage(self.attack)
        return (
            f"{owner.name} played {self.name}. "
            f"It attacks {opponent.name} for {self.attack} damage."
        )

    def __str__(self):
        return (
            f"{self.name} "
            f"(Cost: {self.cost} | Attack: {self.attack}, Health: {self.health}) "
            f"- {self.description}"
        )

    def __repr__(self):
        return (
            f"MinionCard({self.name!r}, cost={self.cost}, "
            f"attack={self.attack}, health={self.health})"
        )


class SpellCard(Card):
    # Card를 상속받아 주문 전용 속성 추가
    def __init__(self, name, cost, description, damage):
        super().__init__(name, cost, description)
        self.damage = damage

    def play(self, owner, target):
        # UI 분리: 출력하지 않고 메시지만 반환
        target.take_damage(self.damage)
        return (
            f"{owner.name} cast {self.name}. "
            f"It deals {self.damage} damage to {target.name}."
        )

    def __str__(self):
        return (
            f"{self.name} "
            f"(Cost: {self.cost} | Damage: {self.damage}) "
            f"- {self.description}"
        )

    def __repr__(self):
        return f"SpellCard({self.name!r}, cost={self.cost}, damage={self.damage})"