# OOPSTONE Project Code

```text
.
|-- main.py
|-- game/
|   |-- card.py
|   |-- card_loader.py
|   |-- console_ui.py
|   |-- deck.py
|   |-- effect.py
|   |-- field.py
|   |-- game_manager.py
|   `-- player.py
`-- data/
    `-- cards.json
```

## FILE: main.py

```python
from game.console_ui import ConsoleUI
from game.game_manager import GameManager


def main():
    # 엔트리포인트: 객체 연결 후 UI 루프 시작
    game_manager = GameManager()
    console_ui = ConsoleUI(game_manager)
    console_ui.run()


if __name__ == "__main__":
    main()
```

## FILE: game/card.py

```python
from abc import ABC, abstractmethod


class Card(ABC):
    # 모든 카드가 공유하는 부모 클래스
    def __init__(self, name : str, cost : int, description : str):
        self.name = name
        self.cost = cost
        self.description = description

    @abstractmethod
    def play(self, owner, target):
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
        self.has_attacked = False

    def play(self, owner, target):
        self.has_attacked = True
        return owner.field.add_minion(self)

    def take_damage(self, amount):
        self.health -= amount

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
        target.take_damage(self.damage)
        return [(
            f"{owner.name} cast {self.name}. "
            f"It deals {self.damage} damage to {target.name}."
        )]

    def __str__(self):
        return (
            f"{self.name} "
            f"(Cost: {self.cost} | Damage: {self.damage}) "
            f"- {self.description}"
        )

    def __repr__(self):
        return f"SpellCard({self.name!r}, cost={self.cost}, damage={self.damage})"
```

## FILE: game/card_loader.py

```python
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
```

## FILE: game/console_ui.py

```python
class ConsoleUI:
    # UI 담당: input()과 print()는 이 클래스에서만 사용
    def __init__(self, game_manager):
        self.game_manager = game_manager

    def run(self):
        print("Console OOPSTONE")
        self.print_messages(self.game_manager.start_turn_messages)

        while not self.game_manager.is_game_over():
            self.show_game_state()
            self.take_turn()

        winner = self.game_manager.get_winner()
        print(f"\nGame over. {winner.name} wins!")

    def show_game_state(self):
        current_player = self.game_manager.get_current_player()
        opponent = self.game_manager.get_opponent()

        print("\n==============================")
        print(f"{current_player.name}'s turn")
        print(f"{current_player.name}: {current_player.health} health, {current_player.mana} mana")
        print(f"{opponent.name}: {opponent.health} health, {opponent.mana} mana")
        print(f"\n{current_player.name}'s field:")
        print(current_player.field.get_display_text())
        print(f"\n{opponent.name}'s field:")
        print(opponent.field.get_display_text())
        print("\nHand:")

        if not current_player.hand:
            print("  No cards in hand.")
            return

        for index, card in enumerate(current_player.hand, start=1):
            print(f"  {index}. {card}")

    def take_turn(self):
        while True:
            choice = input(
                "\nChoose action: 1) Play card from hand "
                "2) Attack with minion Enter) End turn: "
            ).strip()

            if choice == "":
                messages = self.game_manager.end_turn()
                self.print_messages(messages)
                return

            if choice == "1":
                self.play_card()
            elif choice == "2":
                self.play_minion()
            else:
                print("Please enter a valid action.")
                continue

            if self.game_manager.is_game_over():
                return

            self.show_game_state()

    def play_card(self):
        card_number = input("Choose a card number: ").strip()
        current_player = self.game_manager.get_current_player()

        try:
            card_index = int(card_number) - 1
            if card_index < 0 or card_index >= len(current_player.hand):
                raise IndexError
        except (ValueError, IndexError):
            print("Please choose a card number in your hand.")
            return

        success, messages = self.game_manager.play_card(card_index)
        self.print_messages(messages)

    def play_minion(self):
        attacker_number = input("Choose your attacking minion number: ").strip()
        current_player = self.game_manager.get_current_player()

        try:
            attacker_index = int(attacker_number) - 1
            if attacker_index < 0 or attacker_index >= len(current_player.field.minions):
                raise IndexError
        except (ValueError, IndexError):
            print("Please choose a minion number on your field.")
            return

        self.show_attack_targets()
        target_number = input("Choose target number: ").strip()
        opponent = self.game_manager.get_opponent()

        try:
            target_choice = int(target_number)
            if target_choice < 0 or target_choice > len(opponent.field.minions):
                raise IndexError
        except (ValueError, IndexError):
            print("Please choose a valid target number.")
            return

        success, messages = self.game_manager.attack_target(attacker_index, target_choice)
        self.print_messages(messages)

    def show_attack_targets(self):
        opponent = self.game_manager.get_opponent()

        print("\nTargets:")
        print(f"  0. {opponent.name}")
        for index, minion in enumerate(opponent.field.minions, start=1):
            print(f"  {index}. {minion.name} ({minion.attack}/{minion.health})")

    def print_messages(self, messages):
        for message in messages:
            print(message)
```

## FILE: game/deck.py

```python

```

## FILE: game/effect.py

```python

```

## FILE: game/field.py

```python
MAX_MINION = 5
FIELD_FULL_MESSAGE = "Your field is full."


class Field:
    def __init__(self):
        self.minions = []

    def is_full(self):
        return len(self.minions) >= MAX_MINION

    def add_minion(self, minion):
        if self.is_full():
            return [FIELD_FULL_MESSAGE]

        self.minions.append(minion)
        return [f"{minion.name} entered the field."]

    def remove_dead_minions(self):
        messages = []
        alive_minions = []

        for minion in self.minions:
            if minion.health <= 0:
                messages.append(f"{minion.name} died.")
            else:
                alive_minions.append(minion)

        self.minions = alive_minions
        return messages

    def get_display_text(self):
        if not self.minions:
            return "Empty"

        result = []
        for index, minion in enumerate(self.minions, start=1):
            status = "Exhausted" if minion.has_attacked else "Ready"
            result.append(
                f"{index}. {minion.name} "
                f"({minion.attack}/{minion.health}) {status}"
            )

        return "\n".join(result)
```

## FILE: game/game_manager.py

```python
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
```

## FILE: game/player.py

```python
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
```

## FILE: data/cards.json

```json
[
  {
    "name": "Wisp",
    "type": "minion",
    "cost": 0,
    "description": "A tiny free minion.",
    "attack": 1,
    "health": 1
  },
  {
    "name": "Murloc Raider",
    "type": "minion",
    "cost": 1,
    "description": "A cheap aggressive minion.",
    "attack": 2,
    "health": 1
  },
  {
    "name": "Voodoo Doctor",
    "type": "minion",
    "cost": 1,
    "description": "A small support minion.",
    "attack": 2,
    "health": 1
  },
  {
    "name": "Bloodfen Raptor",
    "type": "minion",
    "cost": 2,
    "description": "A solid early-game beast.",
    "attack": 3,
    "health": 2
  },
  {
    "name": "River Crocolisk",
    "type": "minion",
    "cost": 2,
    "description": "A durable early-game minion.",
    "attack": 2,
    "health": 3
  },
  {
    "name": "Ironfur Grizzly",
    "type": "minion",
    "cost": 3,
    "description": "A defensive mid-game minion.",
    "attack": 3,
    "health": 3
  },
  {
    "name": "Chillwind Yeti",
    "type": "minion",
    "cost": 4,
    "description": "A strong vanilla mid-game minion.",
    "attack": 4,
    "health": 5
  },
  {
    "name": "Sen'jin Shieldmasta",
    "type": "minion",
    "cost": 4,
    "description": "A defensive minion with strong health.",
    "attack": 3,
    "health": 5
  },
  {
    "name": "Booty Bay Bodyguard",
    "type": "minion",
    "cost": 5,
    "description": "A large defensive minion.",
    "attack": 5,
    "health": 4
  },
  {
    "name": "Boulderfist Ogre",
    "type": "minion",
    "cost": 6,
    "description": "A powerful late-game minion.",
    "attack": 6,
    "health": 7
  },
  {
    "name": "War Golem",
    "type": "minion",
    "cost": 7,
    "description": "A very large late-game minion.",
    "attack": 7,
    "health": 7
  },
  {
    "name": "Core Hound",
    "type": "minion",
    "cost": 7,
    "description": "A high-attack late-game minion.",
    "attack": 9,
    "health": 5
  },
  {
    "name": "Arcane Shot",
    "type": "spell",
    "cost": 1,
    "description": "Deal 2 damage.",
    "damage": 2
  },
  {
    "name": "Frostbolt",
    "type": "spell",
    "cost": 2,
    "description": "Deal 3 damage.",
    "damage": 3
  },
  {
    "name": "Fireball",
    "type": "spell",
    "cost": 4,
    "description": "Deal 6 damage.",
    "damage": 6
  },
  {
    "name": "Pyroblast",
    "type": "spell",
    "cost": 10,
    "description": "Deal 10 damage.",
    "damage": 10
  }
]
```
