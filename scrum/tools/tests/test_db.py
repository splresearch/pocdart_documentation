"""
test_db.py

This module contains test cases for the database functions using pytest.

Test Cases:
    - test_connect_to_db: Tests the database connection.
    - test_insert_data: Tests the insertion of board data and sprint summary data.
    - test_get_data_from_db: Tests the retrieval of board data and sprint summary data.
"""
import sys
from datetime import date
from pathlib import Path
import pytest

# Add the parent directory to the Python path
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))

from sprint_utils import load_config, load_test_board_data
from trello.db import SprintDBManager


@pytest.fixture(scope='module')
def sprint_db_manager():
    """
    Fixture to create a SprintDBManager instance.

    Returns:
        SprintDBManager: An instance of the SprintDBManager class.
    """
    # Load MySQL configuration
    mysql_config = load_config(parent_path / "config.json")['mysql']
    manager = SprintDBManager(mysql_config)
    return manager


@pytest.fixture
def board_data():
    """
    Fixture to provide test board data.

    Returns:
        dict: A dictionary containing test board data.
    """
    test_board_data = load_test_board_data(
        parent_path / "card_json_archive/test_board_data.json",
        True
    )
    data = {
        'board_id': 'J117',
        'board_name': 'Test Board',
        'json_data': test_board_data
    }
    return data


@pytest.fixture
def sprint_summary_data():
    """
    Fixture to provide test sprint summary data.

    Returns:
        dict: A dictionary containing test sprint summary data.
    """
    data = {
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
    return data


@pytest.fixture
def insert_board_data(sprint_db_manager, board_data):
    """
    Fixture to insert board data into the database and clean up after the test.

    Args:
        sprint_db_manager (SprintDBManager): The database manager fixture.
        board_data (dict): The board data fixture.

    Yields:
        int: The ID of the inserted board record.
    """
    # Insert board data
    board_db_id = sprint_db_manager.insert_data(
        table='boards', insert_data=board_data)
    yield board_db_id
    # Cleanup: delete the inserted board data
    delete_statement = f"DELETE FROM boards WHERE id = {board_db_id};"
    sprint_db_manager.execute_query(query=delete_statement)


@pytest.fixture
def insert_sprint_summary_data(
        sprint_db_manager,
        sprint_summary_data,
        insert_board_data):
    """
    Fixture to insert sprint summary data into the database and clean up after the test.

    Args:
        sprint_db_manager (SprintDBManager): The database manager fixture.
        sprint_summary_data (dict): The sprint summary data fixture.
        insert_board_data (int): The board data insertion fixture.

    Yields:
        int: The ID of the inserted sprint summary record.
    """
    # Insert sprint summary data
    sprint_summary_db_id = sprint_db_manager.insert_data(
        table='sprint_summary',
        insert_data=sprint_summary_data
    )
    yield sprint_summary_db_id
    # Cleanup: delete the inserted sprint summary data
    delete_statement = f"DELETE FROM sprint_summary WHERE id = {
        sprint_summary_db_id};"
    sprint_db_manager.execute_query(query=delete_statement)


def test_connect_to_db(sprint_db_manager):
    """
    Tests the database connection by executing a simple query.

    Args:
        sprint_db_manager (SprintDBManager): The database manager fixture.
    """
    # Act: Execute a simple SELECT query
    select_statement = "SELECT * FROM sprint_summary;"
    # Assert: Verify no error was generated and results are returned
    results = sprint_db_manager.execute_query(query=select_statement)
    assert results is not None


def test_insert_data(
        sprint_db_manager,
        insert_board_data,
        insert_sprint_summary_data):
    """
    Tests the insertion of board data and sprint summary data into the database.

    Args:
        sprint_db_manager (SprintDBManager): The database manager fixture.
        insert_board_data (int): The board data insertion fixture.
        insert_sprint_summary_data (int): The sprint summary data insertion fixture.
    """
    board_db_id = insert_board_data
    sprint_summary_db_id = insert_sprint_summary_data

    # Assert: Verify the board data was inserted correctly
    select_statement = f"SELECT * FROM boards WHERE id = {board_db_id};"
    results = sprint_db_manager.execute_query(query=select_statement)
    assert results is not None
    assert len(results) == 1

    # Assert: Verify the sprint summary data was inserted correctly
    select_statement = f"SELECT * FROM sprint_summary WHERE id = {
        sprint_summary_db_id};"
    results = sprint_db_manager.execute_query(query=select_statement)
    assert results is not None
    assert len(results) == 1


def test_get_data_from_db(
        sprint_db_manager,
        insert_board_data,
        insert_sprint_summary_data):
    """
    Tests the retrieval of board data and sprint summary data from the database.

    Args:
        sprint_db_manager (SprintDBManager): The database manager fixture.
        insert_board_data (int): The board data insertion fixture.
        insert_sprint_summary_data (int): The sprint summary data insertion fixture.
    """
    # Act: Retrieve board data using the board_id
    board_data = sprint_db_manager.get_board_data_from_db(board_id="J117")
    # Assert: Verify the board data was retrieved correctly
    assert board_data is not None
    # Assuming the test board data contains 73 cards
    assert len(board_data) == 73

    # Act: Retrieve sprint summary data using the board_id
    sprint_summaries = sprint_db_manager.get_sprint_summary_from_db(
        board_id="J117")
    # Assert: Verify the sprint summary
    assert sprint_summaries is not None
    assert len(sprint_summaries) == 1
