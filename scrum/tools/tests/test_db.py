"""
test_db.py

This module contains test cases for the database functions.

Test Cases:
    - test_insert_board_data: Tests the insert_board_data function.
    - test_insert_sprint_summary: Tests the insert_sprint_summary function.
    - test_get_board_data_from_db: Tests the get_board_data_from_db function.
    - test_get_sprint_summary_from_db: Tests the get_sprint_summary_from_db function.
"""

import pytest, mysql.connector, sys, os
from unittest.mock import patch, MagicMock
# Get the absolute path of the 'utils' directory relative to this file's location
trello_path = os.path.join(os.path.dirname(os.path.dirname(__file__), 'trello'))

# Add the parent directory to the Python path
sys.path.append(trello_path)

# Import the function from helper.py
from utlis import load_config
from db import SprintDBManger
def test_connect_to_db():
    """
    Tests the connect_to_db function.
    """
    # Arrange: Create a mock connection
    sprint_db_manager = SprintDBManger()

    # Act: Select rows from sprint_summary
    select_statement = "SELECT * FROM sprint_metrics;"
    
    # Assert: Verify no error was generated following Select statement
    results = sprint_db_manager.execute_query(query = select_statement)
    assert results is not None
    

def test_insert_board_data():
    """
    Tests the insert_board_data function.
    """
    # Arrange: Create mock connection

    # Arrange: Set up the board data

    # Act: Call the insert_board_data function
    
    # Assert: Verify the data was inserted correctly
    pass

def test_insert_sprint_summary():
    """
    Tests the insert_sprint_summary function.
    """
    # Arrange: Create mock connection

    # Arrange: Set up the sprint summary data

    # Act: Call the insert_sprint_summary function

    # Assert: Verify the data was inserted correctly
    pass

@patch('trello.db.mysql.connector.connect')
def test_get_board_data_from_db():
    """
    Tests the get_board_data_from_db function.
    """
    # Arrange: Create mock connection

    # Arrange: Set up the expected result

    # Act: Call the get_board_data_from_db function

    # Assert: Verify the data was retrieved correctly
    pass

@patch('trello.db.mysql.connector.connect')
def test_get_sprint_summary_from_db():
    """
    Tests the get_sprint_summary_from_db function.
    """
    # Arrange: Create mock connection

    # Arrange: Set up the expected result

    # Act: Call the get_sprint_summary_from_db function

    # Assert: Verify the data was retrieved correctly
    pass