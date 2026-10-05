# 🎮 Game Glitch Investigator: The Impossible Guesser

## 📖 Project Overview

Game Glitch Investigator is a number-guessing game built with Streamlit. An AI wrote the first version, and it shipped with bugs that made it unwinnable. This repo is the repaired version.

The game picks a secret number in a range set by the difficulty level. You guess, the game says "Go HIGHER!" or "Go LOWER!", and you win by finding the number before you run out of attempts. The secret stays hidden until the game ends.

| Difficulty | Range  | Attempts allowed |
| ---------- | ------ | ---------------- |
| Easy       | 1–20  | 6                |
| Normal     | 1–100 | 8                |
| Hard       | 1–50  | 5                |

**Project structure**

- `app.py`: the Streamlit UI and session state
- `logic_utils.py`: the game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`)
- `tests/`: pytest regression tests for the bugs below

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the game: `python -m streamlit run app.py`
3. Run the tests: `pytest`

## 🎯 Your Mission

1. **Pick a difficulty.** Use the sidebar to choose Easy, Normal or Hard. The range and attempt limit update with it.
2. **Find the secret number.** It is hidden. Use the hints and the guess history to narrow it down.
3. **Win before you run out of attempts.** Fewer attempts means a higher score.
4. **Play again.** Click **New Game** for a fresh secret and a clean score.

## 🐛 Bugs Found and Fixed

- **Reversed hints.** "Go HIGHER" and "Go LOWER" pointed the wrong way. The comparison logic in `check_guess` is corrected.
- **Secret turned into a string.** On every even attempt the secret was cast to `str`, so comparisons were wrong. The cast is removed.
- **Difficulty change didn't reset the game.** Switching difficulty kept the old secret, which could fall outside the new range. The game now resets when difficulty changes.
- **New Game didn't fully reset.** Attempts, score, history, status and the guess box are now all cleared.
- **Stale "Attempts left" display.** The status panel was drawn before the state updated. It is now rendered after the guess is processed.
- **Logic mixed into the UI.** The helper functions now live in `logic_utils.py` so they can be tested.

## 📸 Demo Walkthrough

1. Launch the app with `python -m streamlit run app.py`. The page opens with the title and a "Make a guess" section.
2. In the sidebar, choose a difficulty, for example **Normal**. The sidebar shows "Range: 1 to 100" and "Attempts allowed: 8".
3. Type a number in the **Enter your guess** box and click **Submit Guess 🚀**.
4. Read the hint, for example "📉 Go HIGHER!". The status banner updates the attempts left, and the guess is added to the history in the **Developer Debug Info** expander. The secret is not shown there.
5. Keep guessing, using each hint to narrow the range. Non-numeric or empty input shows an error message.
6. If you find the number, balloons appear and you see your final score. If you run out of attempts, the game ends and reveals the secret.
7. Click **New Game 🔁** to reset, or change the difficulty, which also starts a fresh game.

## 🧪 Test Results

```
============================= test session starts ==============================
platform darwin -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/jeanmariengabonziza/CodePath/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.15.1
collected 19 items

tests/test_game_logic.py ...................                             [100%]

============================== 19 passed in 2.04s ==============================
```
