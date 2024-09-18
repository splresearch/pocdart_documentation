"""
test_board.py

This module contains test cases for the `Board` class using pytest.

Test Cases:
    - `test_fetch_data`: Tests the `fetch_data` method of the `Board` class.
    - `test_extract_cards`: Tests the `extract_cards` method of the `Board` class.
    - `test_calculate_story_points`: Tests the `calculate_story_points` 
        method of the `Board` class using stored board data.
"""

import sys
from pathlib import Path

import pytest

# Adjust the sys.path to include the parent directory
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))

from sprint_utils import load_config, load_test_board_data
from trello.api import TrelloAPI
from trello.board import Board
from trello.card import Card


@pytest.fixture(scope='module')
def trello_api():
    """
    Fixture to create a TrelloAPI instance.

    Returns:
        TrelloAPI: An instance of the TrelloAPI class.
    """
    # Load board configuration
    board_config = load_config(parent_path / "config.json")['board']

    # Create TrelloAPI instance
    api = TrelloAPI(
        board_id=board_config['board_id'],
        api_key=board_config['api_key'],
        api_token=board_config['api_token']
    )
    return api


def test_fetch_data(trello_api):
    """
    Tests the `fetch_data` method of the `Board` class.

    Args:
        trello_api (TrelloAPI): Fixture providing a `TrelloAPI` instance.

    Notes:
        This test fetches data from the live Trello board. Ensure that the API credentials are valid
        and that the board contains data before running this test.
    """
    # Act: Create Board instance, which fetches data from the live board
    board = Board(trello_api)

    # Assert: Verify the data was fetched and stored correctly
    data = board.get_data()
    assert data is not None
    assert len(data) > 0


def test_extract_cards(trello_api):
    """
    Tests the `extract_cards` method of the `Board` class.

    Args:
        trello_api (TrelloAPI): Fixture providing a `TrelloAPI` instance.

    Notes:
        This test depends on the live Trello board data. 
            Ensure that the board contains cards to extract.
    """
    # Arrange: Create a Board instance with data from the live board
    board = Board(trello_api)

    # Act: Call the `extract_cards` method
    board.extract_cards()

    # Assert: Verify the cards were extracted correctly
    cards = board.get_cards()
    assert cards is not None
    assert len(cards) > 0
    assert isinstance(cards[0], Card)


def test_calculate_story_points(trello_api):
    """
    Tests the `calculate_story_points` method of the `Board` class using stored board data.

    Args:
        trello_api (TrelloAPI): Fixture providing a `TrelloAPI` instance.

    Notes:
        This test uses stored test data from `test_board_data.json`. 
            Ensure that this file exists and contains valid data.
    """
    # Arrange: Load test board data
    test_board_data = load_test_board_data(
        parent_path / "card_json_archive/test_board_data.json")

    # Create a Board instance with the test data
    board = Board(trello_api, test_board_data)
    board.extract_cards()

    # Define expected results
    expected = {
        'unplanned': {'total': 20, 'spent': 16, 'remaining': 4},
        'planned': {'total': 29, 'spent': 24, 'remaining': 5},
        'retro': {'total': 4, 'spent': 0, 'remaining': 4}
    }

    # Act: Call the `calculate_story_points` method
    results = board.calculate_story_points()

    # Assert: Verify the calculated story points match the expected results
    assert results is not None
    assert len(results) > 0
    assert results == expected
