from game.console_ui import ConsoleUI
from game.game_manager import GameManager


def main():
    # 엔트리포인트: 객체 연결 후 UI 루프 시작
    game_manager = GameManager()
    console_ui = ConsoleUI(game_manager)
    console_ui.run()


if __name__ == "__main__":
    main()
