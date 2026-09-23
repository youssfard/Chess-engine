A classic game of Chess with a graphical interface, full legal move generation, and check/checkmate detection.

This is a preview of the game's main page.

<img width="794" height="798" alt="Chess game main page preview" src="https://github.com/user-attachments/assets/66ced87f-5c6a-45ff-8600-33a220546a7b" />

Built with Python, applying core OOP principles to model the board, pieces, and move logic.

## Features

- Full 8x8 board with all standard pieces (pawn, rook, knight, bishop, queen, king)
- Legal move generation per piece type, including move filtering so you can't make a move that leaves your own king in check
- Check and checkmate detection
- Click-to-select and click-to-move interaction with move highlighting on the board
- Turn-based play (white / black)

## Tech Stack

- Python 3.10
- Pygame for the GUI and rendering

## Project Structure

- `main.py` — entry point, wires up the GUI and game controller
- `gamecontroller.py` — core game state: board, turns, move legality, check/checkmate detection
- `move_manager.py` — per-piece move generation (pawn, rook, knight, bishop, queen, king)
- `gui.py` — Pygame rendering: board, pieces, move highlighting, input handling
- `pieces/` — piece images
