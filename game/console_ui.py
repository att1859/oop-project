class ConsoleUI:
    # UI 담당: input()과 print()는 이 클래스에서만 사용
    def __init__(self, game_manager):
        self.game_manager = game_manager

    def run(self):
        print("Console Hearthstone-like Card Battle")

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
        print("\nHand:")

        if not current_player.hand:
            print("  No cards in hand.")
            return

        for index, card in enumerate(current_player.hand, start=1):
            print(f"  {index}. {card}")

    def take_turn(self):
        while True:
            choice = input("\nChoose a card number to play, or press Enter to end turn: ").strip()

            if choice == "":
                # 빈 입력: 턴 넘김
                self.game_manager.end_turn()
                return

            if not choice.isdigit():
                print("Please enter a valid card number.")
                continue

            # 사용자 선택은 1부터, 리스트 인덱스는 0부터 시작
            card_index = int(choice) - 1
            success, message = self.game_manager.play_card(card_index)
            print(message)

            if success:
                if self.game_manager.is_game_over():
                    return
                self.game_manager.end_turn()
                return
