"""
test_db.py

This module contains test cases for the database functions.

Test Cases:
    - test_insert_board_data: Tests the insert_board_data function.
    - test_insert_sprint_summary: Tests the insert_sprint_summary function.
    - test_get_board_data_from_db: Tests the get_board_data_from_db function.
    - test_get_sprint_summary_from_db: Tests the get_sprint_summary_from_db function.
"""

import pytest, mysql.connector, sys, os, json
from datetime import date, datetime
from unittest.mock import patch, MagicMock

# Import the function from helper.py
# Get the absolute path of the 'utils' directory relative to this file's location
parent_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))

# Add the parent directory to the Python path
sys.path.append(parent_path)
from sprint_utlis import load_config, load_test_board_data
from trello.db import SprintDBManger

sprint_db_manager = SprintDBManger()
# Arrange: Create mock connection and get test board data
test_board_data = load_test_board_data("../card_json_archive/test_board_data.json", True)
# Arrange: Set up the board data
board_data = {
    'board_id': 'J117',
    'board_name': 'Test Board',
    'json_data': test_board_data
}
# Arrange: Set up the mock sprint summary data
sprint_summary_data = {
    'board_id': 'J117',
    'start_date': date.today().strftime('%Y-%m-%d'),
    'length_days': 15,
    'members': 8,
    'vacation_days': 0,
    'planned_total': 20,
    'planned_completed': 16,
    'planned_remaining': 4,
    'unplanned_total': 8,
    'unplanned_completed': 6,
    'unplanned_remaining': 2,
    'retro_total': 4,
    'retro_completed': 4,
    'retro_remaining': 0
}

@pytest.fixture()
def teardown():
    delete_data = {
        "board_db_id": None,
        "sprint_summary_db_id": None
    }

    yield delete_data

    # Clean out inserted data
    if delete_data["sprint_summary_db_id"] is not None:
        delete_statement = f"DELETE FROM sprint_summary WHERE id = {delete_data["sprint_summary_db_id"]};"
        sprint_db_manager.execute_query(query = delete_statement)

    if delete_data["board_db_id"] is not None:
        delete_statement = f"DELETE FROM boards WHERE id = {delete_data["board_db_id"]};"
        sprint_db_manager.execute_query(query = delete_statement)

@pytest.fixture()
def setup_and_teardown_boards(teardown):

    # Act: Call the insert_board_data function
    teardown["board_db_id"] = sprint_db_manager.insert_data(table='boards', insert_data=board_data)

    yield teardown

@pytest.fixture()
def setup_and_teardown_summaries(setup_and_teardown_boards):

    # Act: Call the insert_board_data function
    setup_and_teardown_boards["sprint_summary_db_id"] = sprint_db_manager.insert_data(table='sprint_summary', insert_data=sprint_summary_data)

    yield setup_and_teardown_boards


def test_connect_to_db():
    """
    Tests the connect_to_db function.
    """

    # Act: Select rows from sprint_summary
    select_statement = "SELECT * FROM sprint_summary;"
    
    # Assert: Verify no error was generated following Select statement
    results = sprint_db_manager.execute_query(query = select_statement)
    assert results is not None

def test_insert_data(teardown):
    # Act: Call the insert_board_data function
    teardown["board_db_id"] = sprint_db_manager.insert_data(table='boards', insert_data=board_data)

    # Assert: Verify the data was inserted correctly
    select_statement = f"SELECT * FROM boards WHERE id = '{teardown["board_db_id"]}';"
    
    results = sprint_db_manager.execute_query(query = select_statement)
    assert results is not None
    assert len(results) == 1

    # Act: Call the insert_board_data function
    teardown["sprint_summary_db_id"] = sprint_db_manager.insert_data(table='sprint_summary', insert_data=sprint_summary_data)

    # Assert: Verify the data was inserted correctly
    select_statement = f"SELECT * FROM sprint_summary WHERE id = '{teardown["sprint_summary_db_id"]}';"
    
    results = sprint_db_manager.execute_query(query = select_statement)
    assert results is not None
    assert len(results) == 1

def test_get_data_from_db(setup_and_teardown_summaries):

    # Assert: Verify the data was inserted correctly
    results = sprint_db_manager.get_board_data_from_db(board_id="J117")
    assert results is not None
    assert len(results) == 1

    # Assert: Verify the data was inserted correctly
    results = sprint_db_manager.get_sprint_summary_from_db(board_id="J117")
    assert results is not None
    assert len(results) == 1