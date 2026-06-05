# OOPSTONE

## Overview
OOPSTONE은 Hearthstone을 참고한 콘솔 기반 턴제 카드 게임입니다.
Python 객체지향 구조를 사용해 카드, 플레이어, 필드, 게임 진행, 콘솔 UI를 분리했습니다.

## Features
- Player 1 vs Player 2 턴제 진행
- 마나 기반 카드 사용
- 하수인 카드와 주문 카드
- 하수인 소환, 영웅 공격, 하수인 전투
- JSON 파일을 통한 카드 데이터 로딩
- 콘솔 UI와 게임 로직 분리

## Project Structure
```text
oopstone/
|-- main.py
|-- game/
|   |-- card.py
|   |-- card_loader.py
|   |-- console_ui.py
|   |-- deck.py          # 현재 미구현
|   |-- effect.py        # 현재 미구현
|   |-- field.py
|   |-- game_manager.py
|   `-- player.py
|-- data/
|   `-- cards.json
`-- README.md
```

## How to Run
```bash
python main.py
```

## Main Classes
| Class | Responsibility |
|---|---|
| Card | 모든 카드의 기본 클래스 |
| MinionCard | 필드에 소환되는 하수인 카드 |
| SpellCard | 즉시 피해를 주는 주문 카드 |
| CardLoader | JSON 카드 데이터를 객체로 변환 |
| Player | 체력, 마나, 덱, 손패, 필드 관리 |
| Field | 하수인 배치와 사망 처리 |
| GameManager | 턴 진행, 카드 사용, 전투, 승패 관리 |
| ConsoleUI | 콘솔 입력과 출력 처리 |

## Future Improvements
- 덱 전용 클래스 구현
- 효과 시스템 구현
- 간단한 AI 추가
- 카드 종류 확장
- 저장/불러오기 기능 추가

## Reference
[1] J. Seo, Object-Oriented Programming Lecture Slides, Konkuk University, Spring 2026.
[2] Blizzard Entertainment, Hearthstone Official Website. Available: https://hearthstone.
blizzard.com/
[3] Python Software Foundation, Python 3 Documentation. Available: https://docs.python.org/3/
[4] S. F. Lott and D. Phillips, Python Object-Oriented Programming: Build Robust and Maintainable
Object-Oriented Python Applications and Libraries, 4th ed. Birmingham, UK: Packt Publishing,
2021.