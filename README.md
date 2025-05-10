# War of Colors

A Python-based card game created using Pygame, featuring regular and special cards, score tracking, and game logic for both human and computer players.

## Objective

Two players (you vs the computer) take turns playing cards from their hands. Points are awarded when matching colored cards are played, with bonuses for repeating numbers and various special cards that affect the flow. The player with the highest score at the end wins!

---

## Features

- 🎮 Intuitive Pygame-based GUI
- 🃏 Regular and 4 types of special cards (`Wild`, `Watcher`, `Colorstorm`, `Ascendancy`)
- 🔄 Shuffle deck using **Fisher-Yates** algorithm
- ♻️ Dynamic draw stack and discard pile
- 🤖 AI randomly selects a card to play
- 🎨 Card selection, play button interaction, and result display
- 🧠 Bonus point logic and state tracking across rounds
- 📈 Game over detection and replay option
- 🔊 Background music for improved game experience

---

## Libraries Used

- `pygame` – For rendering GUI and handling game events
- `random`, `sys`, `os`, `time` – For core game mechanics and utilities

All libraries are standard or commonly used and are applied with efficiency in mind.

---

## Algorithms

- **Fisher-Yates Shuffle Algorithm**  
  Ensures fairness in card distribution through an in-place shuffle (`shuffle()` function).
  
- **Round Resolution & Scoring Algorithm**  
  Compares cards based on game rules, awards points, applies bonus logic, and transitions states accordingly (`resolve_round()`).

- **Card Selection & Collision Detection**  
  Mouse click detection and collision rectangles allow accurate card selection and game interactions (`handle_card_selection()`).

---

## Data Structures

- `List` – Used for managing:
  - Player and computer hands
  - Draw stack
  - Discard pile

- `Class` – `Card` class used for encapsulating card properties and rendering logic, supporting multiple card types.

The program uses **two or more standard data structures (Lists, Classes)** and leverages them effectively to support game logic and rendering.

---

## Code Structure & Readability

- Follows **PEP8** style guide
- Accurate variable names (e.g., `player_score`, `game_state`, `played_card_message`)
- All functions/classes include **clear docstrings** and **consistent formatting**
- Modularized logic:
  - `deal_cards()`, `draw_player_hand()`, `play_selected_card()`, etc.
  - Enables separation of concerns and better maintenance

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/aydinefendi/Python-Project.git
   cd Python-Project
