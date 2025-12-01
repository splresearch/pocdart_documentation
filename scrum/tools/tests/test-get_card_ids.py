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
import re
from pathlib import Path
import pytest

# Add the parent directory to the Python path
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))

from bin.get_card_ids import main

def test_main(capfd):
    # Call target method
    main()
    # Check for presence of trello card short link in pipe-delimited output
    captured = capfd.readouterr()
    expected_message = r"Q9EAW7j2\|"
    assert re.search(expected_message, captured.out)