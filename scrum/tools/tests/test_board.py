"""
test_board.py

This module contains test cases for the Board class.

Test Cases:
    - test_fetch_data: Tests the fetch_data method of the Board class.
    - test_calculate_story_points: Tests the calculate_story_points method of the Board class using stored boards from the database.
"""

import pytest, sys, os
# Import the function from helper.py
# Get the absolute path of the 'utils' directory relative to this file's location
parent_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))

# Add the parent directory to the Python path
sys.path.append(parent_path)
from sprint_utlis import load_config
from trello.board import Board
from trello.api import TrelloAPI
from trello.db import SprintDBManger
from trello.card import Card

# Arrange: Pull board config info
board_config = load_config("../config.json")['board']

# Arrange: Set up the mock response data
trello_api = TrelloAPI(
    board_id = board_config['board_id'],
    api_key = board_config['api_key'],
    api_token = board_config['api_token']
)

def test_fetch_data():
    """
    Tests the fetch_data method of the Board class.
    """
    # Act: Create Board instance, which has it fetch data from the live board
    board = Board(trello_api)

    # Assert: Verify the data was fetched and stored correctly
    assert board.get_data() is not None
    assert len(board.get_data()) > 0
    

def test_extract_cards():
    """
    Tests the extract_cards method of the Board class.
    """
    # Arrange: Create a Board instance with the provided data
    board = Board(trello_api)

    # Act: Call the extract_cards method
    board.extract_cards()

    # Assert: Verify the cards were extracted correctly
    assert board.get_cards() is not None
    assert len(board.get_cards()) > 0
    assert isinstance(board.get_cards()[0], Card)

    

def test_calculate_story_points():
    """
    Tests the calculate_story_points method of the Board class using stored boards from the database.
    """
        
    # Arrange: Create a Board instance with the retrieved data

    # Act: Call the calculate_story_points method
    
    # Assert: Verify the calculated story points match the expected results
    pass
