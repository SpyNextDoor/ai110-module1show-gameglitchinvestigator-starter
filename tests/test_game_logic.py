import os
import sys

import pytest
from streamlit.testing.v1 import AppTest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_utils import check_guess, get_range_for_difficulty

APP_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py")


def new_app():
    return AppTest.from_file(APP_PATH, default_timeout=10).run()


def submit_guess(at, value):
    at.text_input[0].set_value(str(value))
    at.button[0].click().run()
    return at


def debug_text(at):
    panel = at.expander[0]
    return " ".join([m.value for m in panel.markdown] + [str(j.value) for j in panel.json])


# ---------------------------------------------------------------------------
# Baseline check_guess behaviour (returns an (outcome, message) tuple)
# ---------------------------------------------------------------------------
def test_winning_guess():
    assert check_guess(50, 50)[0] == "Win"


def test_guess_too_high():
    assert check_guess(60, 50)[0] == "Too High"


def test_guess_too_low():
    assert check_guess(40, 50)[0] == "Too Low"


# ---------------------------------------------------------------------------
# Bug 1: hints were backwards / random
# ---------------------------------------------------------------------------
def test_hint_says_go_lower_when_guess_is_too_high():
    outcome, message = check_guess(80, 30)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_hint_says_go_higher_when_guess_is_too_low():
    outcome, message = check_guess(10, 70)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_hint_is_consistent_across_repeated_calls():
    results = {check_guess(90, 20) for _ in range(20)}
    assert len(results) == 1

# ---------------------------------------------------------------------------
# Bug 2: "New Game" button did nothing
# ---------------------------------------------------------------------------
def test_new_game_resets_state():
    at = new_app()
    submit_guess(at, 1)
    assert at.session_state.attempts > 1
    assert len(at.session_state.history) == 1

    at.button[1].click().run()

    assert not at.exception
    assert at.session_state.attempts == 1
    assert at.session_state.score == 0
    assert at.session_state.history == []
    assert at.session_state.status == "playing"


def test_new_game_after_game_over_allows_playing_again():
    at = new_app()
    # Normal allows 8 attempts; burn them all with non-winning guesses.
    secret = at.session_state.secret
    wrong = 1 if secret != 1 else 2
    for _ in range(8):
        if at.session_state.status != "playing":
            break
        submit_guess(at, wrong)
    assert at.session_state.status == "lost"

    at.button[1].click().run()

    assert at.session_state.status == "playing"
    assert at.session_state.attempts == 1


def test_new_game_clears_guess_input():
    at = new_app()
    submit_guess(at, 5)
    at.button[1].click().run()
    assert at.text_input[0].value == ""


# ---------------------------------------------------------------------------
# Bug 3: developer debug panel lagged one guess behind
# ---------------------------------------------------------------------------
def test_debug_panel_shows_won_immediately_after_correct_guess():
    at = new_app()
    secret = at.session_state.secret
    # Attempt 2 is the first submit; app passes the secret as str on even
    # attempts, so make a throwaway wrong guess first to land on a normal one.
    wrong = 1 if secret != 1 else 2
    submit_guess(at, wrong)
    submit_guess(at, secret)

    assert at.session_state.status == "won"
    assert "won" in debug_text(at)


def test_debug_panel_history_updates_on_same_run_as_submit():
    at = new_app()
    submit_guess(at, 7)
    assert "7" in debug_text(at)
    submit_guess(at, 8)
    text = debug_text(at)
    assert "7" in text and "8" in text


def test_debug_panel_attempts_updates_immediately():
    at = new_app()
    submit_guess(at, 7)
    assert f"{at.session_state.attempts}" in debug_text(at)
    assert at.session_state.attempts == 2


def test_status_is_initialised_without_attribute_error():
    at = new_app()
    assert not at.exception
    assert at.session_state.status == "playing"


# ---------------------------------------------------------------------------
# Bug 4: changing difficulty must reset the game with a secret in range
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "difficulty,low,high",
    [("Easy", 1, 20), ("Normal", 1, 100), ("Hard", 1, 50)],
)
def test_range_for_difficulty(difficulty, low, high):
    assert get_range_for_difficulty(difficulty) == (low, high)


@pytest.mark.parametrize("difficulty", ["Easy", "Hard"])
def test_changing_difficulty_resets_game_and_secret_in_range(difficulty):
    low, high = get_range_for_difficulty(difficulty)
    at = new_app()
    submit_guess(at, 3)
    assert at.session_state.attempts > 1

    # Repeat to make sure the secret is always within the new boundaries.
    for _ in range(25):
        at.sidebar.selectbox[0].select("Normal").run()
        at.sidebar.selectbox[0].select(difficulty).run()
        assert not at.exception
        assert at.session_state.game_difficulty == difficulty
        assert low <= at.session_state.secret <= high
        assert at.session_state.attempts == 1
        assert at.session_state.score == 0
        assert at.session_state.history == []
        assert at.session_state.status == "playing"


def test_changing_difficulty_after_loss_starts_fresh_game():
    at = new_app()
    secret = at.session_state.secret
    wrong = 1 if secret != 1 else 2
    for _ in range(8):
        if at.session_state.status != "playing":
            break
        submit_guess(at, wrong)
    assert at.session_state.status == "lost"

    at.sidebar.selectbox[0].select("Easy").run()

    assert at.session_state.status == "playing"
    assert 1 <= at.session_state.secret <= 20
