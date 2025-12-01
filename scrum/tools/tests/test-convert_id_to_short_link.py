"""
test_api.py

This module contains unit tests for the TrelloAPI class, ensuring that the API interactions
with Trello are correctly implemented.

Tests:
    - test_get_board_cards: Tests the get_board_cards method.
    - test_get_board_lists: Tests the get_board_lists method.
    - test_get_card_story_points: Tests the get_card_story_points method.
"""

import sys
from pathlib import Path
import pytest

# Add the parent directory to the Python path
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))

from bin.convert_id_to_short_link import main
from sprint_utils import load_config

board_config = load_config("config.json")['board']

def test_main(capfd):
    # Call target method
    main(board_config["slack_card"])
    # Check for printout of associated trello card short link
    captured = capfd.readouterr()
    expected_message = "Q9EAW7j2"
    assert expected_message in captured.out