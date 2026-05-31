# OOPSTONE Codex Instructions

## Project Goal
Build a console-based Hearthstone-like card battle game in Python.
The main purpose is to demonstrate object-oriented programming concepts for a university OOP assignment.

## Development Priorities
1. Keep the implementation simple and readable.
2. Implement the console version first.
3. Separate core game logic from UI.
4. Do not add Pygame until the console game works.
5. Avoid over-engineering.

## Architecture Rules
- `game/card.py` contains card classes.
- `game/player.py` contains the Player class.
- `game/deck.py` contains the Deck class.
- `game/game_manager.py` controls turn flow and win/loss logic.
- `game/console_ui.py` handles input/output only.
- `main.py` starts the game.

## OOP Requirements
Use the following OOP concepts clearly:
- Inheritance: `Card` → `SpellCard`, `MinionCard`
- Polymorphism: each card implements `play()`
- Composition: `Player` has a `Deck`, `hand`, and `field`
- Encapsulation: HP, mana, and deck operations should be changed through methods
- Manager object: `GameManager` controls the game workflow

## Style Rules
- Use type hints.
- Keep functions short.
- Do not put `input()` or `print()` inside card classes.
- Card classes should return result messages instead of printing directly.
- Prefer standard library only for the first version.

## First Milestone
Implement a minimal playable console game:
- Player vs Enemy
- HP and mana
- A small starter hand
- Damage card
- Heal card
- Turn progression
- Enemy performs a simple attack
- Game ends when one side reaches 0 HP

## Do Not Do Yet
- Do not implement Pygame.
- Do not implement complex AI.
- Do not implement online multiplayer.
- Do not implement full Hearthstone rules.