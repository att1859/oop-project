# Hearthstone-like "OOPSTONE" card game

## 1. Project Overview
이 프로젝트는 하스스톤을 모티브로 한 콘솔 베이스 카드 게임이다. Python의 객체지향 프로그래밍 원칙을 사용하여 카드, 플레이어, 덱, 턴 진행, 전투 로그를 객체로 분리해 구현한다.
## 2. Motivation
카드, 플레이어, 덱, 턴, 필드 등을 모델링하면서 OOP 디자인을 구현해보는 것이 목표이다.
## 3. Main Features
- 플레이어 vs 적
- 덱과 핸드 시스템
- 마나 기반 카드 사용
- 하수인 카드와 마법 카드
- 하수인의 공격, 피격 및 사망 시스템
- 턴제 게임
- 배틀 로그
- UI와 게임 로직의 분리
## 4. OOP Design
이 프로젝트는 상속과 다형성을 사용하여 다양한 카드 유형을 표현한다. 각 카드는 고유한 play() 동작을 구현하며, 게임 관리자는 게임 진행 상황을 총괄한다.
## 5. Project Structure
```
hearthstone_oop/
│
├─ main.py
├─ game/
│  ├─ card.py
│  ├─ player.py
│  ├─ deck.py
│  ├─ game_manager.py
│  └─ console_ui.py
│
├─ data/
│  └─ cards.json
│
├─ README.md
└─ requirements.txt
```
## 6. How to Run
in bash `python main.py`
## 7. Example Gameplay
## 8. Key Classes
| Class | Responsibility |
|---|---|
| Card | Base class for all cards |
| MinionCard | Represents a summonable minion card |
| SpellCard | Represents a one-time effect card |
| Player | Manages HP, mana, deck, and hand |
| Deck | Stores and draws cards |
| GameManager | Controls turn flow and win/loss logic |
| ConsoleUI | Handles console input and output |
## 9. Future Improvements
- Add Pygame graphical interface
- Add enemy AI strategy
- Add more card effects
- Add save/load system
- Add deck-building feature
## 10. References
- Heathstone