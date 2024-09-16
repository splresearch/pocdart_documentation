"""
test_api.py

This module contains unit tests for the TrelloAPI class, ensuring that the API interactions
with Trello are correctly implemented.

Tests:
    - test_get_cards: Tests the get_board_cards method.
    - test_get_lists: Tests the get_board_lists method.
    - test_get_card_story_points: Test the get_card_story_points method.
"""

import pytest, os, sys
# Import the function from helper.py
# Get the absolute path of the 'utils' directory relative to this file's location
parent_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))

# Add the parent directory to the Python path
sys.path.append(parent_path)
from trello.api import TrelloAPI
from sprint_utlis import load_config

from pathlib import Path

# Arrange: Pull board config info
board_config = load_config(Path(__file__).parent.parent / "config.json")['board']

# Arrange: Set up mock response data
trello_api = TrelloAPI(
    board_id = board_config['board_id'],
    api_key = board_config['api_key'],
    api_token = board_config['api_token']
)

def test_get_cards():

    # Act: Call get_board_cards method
    sprint_cards = trello_api.get_board_cards()
    
    # Assert: Verify that the response data matches expected values
    assert sprint_cards is not None
    assert len(sprint_cards) > 0
    assert sprint_cards[0]["id"] == board_config['sprint_calc_card']

def test_get_lists():

    # Act: Call get_board_cards method
    sprint_lists = trello_api.get_board_lists()
    
    # Assert: Verify that the response data matches expected values
    assert sprint_lists is not None
    assert len(sprint_lists) > 0

def test_get_card_story_points():
    # Arrange: Get test card id
    test_card_id = board_config['slack_card']
    # Act: Call get_board_cards method
    sprint_cards = trello_api.get_card_story_points("Slack Channel Assignments", test_card_id)
    
    # Assert: Verify that the response data matches expected values
    assert sprint_cards is not None
    assert len(sprint_cards) > 0
    assert sprint_cards['total'] == 1
    assert sprint_cards['spent'] == 1
    assert sprint_cards['remaining'] == 0