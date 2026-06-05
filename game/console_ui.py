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
