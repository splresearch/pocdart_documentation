"""
main.py

This is the main module for running the Trello data extraction and storage process. It sets up
the Trello API, fetches board and card data, calculates story points, and stores the data in
a MySQL database.

Functions:
    - main: The main entry point for the script.
    - validate_user_input: Validates user input to ensure it's an integer.
    - prompt_for_sprint_controls: Prompts the user for sprint control values.
    - prompt_for_board_source: Determines the source of the board data.
    - prompt_for_manual_corrections: Allows manual corrections to story points.
    - show_sp_calculations: Displays the calculated story points.
    - prompt_for_board_insert: Determines whether to insert board data into the database.
    - get_board_data: Retrieve board data either from the database or from the live Trello board.
    - compute_recommendation: Compute the recommended number of story points for the next sprint.
    - insert_sprint_summary: Insert the sprint summary data into the database.

Example:
    if __name__ == "__main__":
        main()
"""

import statistics
import math
import json
from datetime import date

from trello.db import SprintDBManager
from trello.api import TrelloAPI
from trello.board import Board
from sprint_utils import load_config

def validate_user_input(user_input):
    """Validates the user input to ensure it is a valid integer.

    Args:
        user_input (str): The input provided by the user.

    Returns:
        int: The validated user input as an integer.
    """
    while True:
        try:
            validated_input = int(user_input)
            return validated_input
        except ValueError:
            user_input = input("Invalid input; enter a number: ")


def prompt_for_sprint_controls():
    """
    Prompts the user for sprint control values.

    Returns:
        dict: A dictionary containing sprint control values with descriptive keys.
    """
    variables = {
        "last_sprint_days": "last Sprint days",
        "next_sprint_days": "next Sprint days",
        "missed_last_sprint": "total days missed last Sprint",
        "missed_next_sprint": "total days planned missed next Sprint",
        "members": "members working this coming Sprint"
    }
    defaults = [15, 15, 0, 0, 8]

    sprint_controls = {}

    # Loop through the variables and prompt the user for each value
    for i, (var_name, description) in enumerate(variables.items()):
        default = defaults[i]
        user_input = input(
            f"Enter number of {description} (default: {default}): ")
        if user_input == "":
            sprint_controls[var_name] = default
        else:
            validated_input = validate_user_input(user_input)
            sprint_controls[var_name] = validated_input

    return sprint_controls


def prompt_for_board_source():
    """
    Determines the source of the board data based on user input.

    Returns:
        int: 0 if the user wants to load from the database, 1 otherwise.
    """
    choice = None
    while choice not in ('Y', 'N'):
        print("Would you like to pull data from the database instead of the current board?")
        choice = input("Enter Y or N: ").strip().upper()
        if choice == 'Y':
            result = 0
        elif choice == 'N':
            result = 1
        else:
            print("Invalid input; please enter 'Y' or 'N'.")
    return result


def prompt_for_manual_corrections(story_points):
    """
    Allows the user to manually correct the calculated story points.

    Args:
        story_points (dict): The calculated story points.

    Returns:
        dict: The story points after any manual corrections.
    """
    # Ask user if they want to make edits to the story points
    choice = input(
        "Do you want to make edits to the calculated story points? (Y/N): ").strip().upper()
    if choice != "Y":
        return story_points

    for category, sp_attr in story_points.items():
        print(f"Modifying entries for '{category}':")
        for inner_key, value in sp_attr.items():
            print(f"Current value of '{inner_key}': {value}")
            # Ask user if they want to change the current value
            change = input(
                "Do you want to change this value? (Y/N): ").strip().upper()
            if change == 'Y':
                # Get the new value from the user
                new_value = input(
                    f"Enter the new value for '{inner_key}': ").strip()
                try:
                    # Convert input to a number if possible
                    new_value = int(new_value)
                except ValueError:
                    print("Invalid input, keeping the original value.")
                else:
                    sp_attr[inner_key] = new_value
            print()  # Add a blank line for better readability
    return story_points


def show_sp_calculations(story_points, recommendation=None):
    """
    Displays the calculated story points in a formatted manner.

    Args:
        story_points (dict): The calculated story points.
        recommendation (int, optional): The recommended story points for the next sprint.
    """
    results = (
        f"SP Planned  : {str(story_points['planned']['total']).rjust(2)}(T), "
        f"{str(story_points['planned']['spent']).rjust(2)}(A), "
        f"{str(story_points['planned']['remaining']).rjust(2)}(LO)\n"
        f"SP Unplanned: {
            str(story_points['unplanned']['total']).rjust(2)}(T), "
        f"{str(story_points['unplanned']['spent']).rjust(2)}(A), "
        f"{str(story_points['unplanned']['remaining']).rjust(2)}(LO)\n"
        f"SP Retro    : {str(story_points['retro']['total']).rjust(2)}(T), "
        f"{str(story_points['retro']['spent']).rjust(2)}(A), "
        f"{str(story_points['retro']['remaining']).rjust(2)}(LO)\n"
    )
    if recommendation is not None:
        results += (
            "======================\n"
            f"SP: Target for next sprint: {str(recommendation)}\n"
        )
    print(results)


def prompt_for_board_insert():
    """
    Determines whether to insert the board data into the database based on user input.

    Returns:
        int: 0 if the user wants to insert the board data, 1 otherwise.
    """
    choice = None
    while choice not in ('Y', 'N'):
        print("Would you like to insert board data into the board database?")
        choice = input("Enter Y or N: ").strip().upper()
        if choice == 'Y':
            result = 0
        elif choice == 'N':
            result = 1
        else:
            print("Invalid input; please enter 'Y' or 'N'.")
    return result


def main():
    # Load configuration
    config = load_config("config.json")
    mysql_config = config['mysql']
    board_config = config['board']

    # Initialize database manager and Trello API
    sprint_db_manager = SprintDBManager(mysql_config)
    trello_api = TrelloAPI(
        board_id=board_config['board_id'],
        api_key=board_config['api_key'],
        api_token=board_config['api_token']
    )

    # Collect user inputs
    sprint_controls = prompt_for_sprint_controls()
    board_source = prompt_for_board_source()

    # Get board data
    board_data = get_board_data(sprint_db_manager, trello_api, board_source)

    # Process board data
    board = Board(trello_api, board_data)
    board.extract_cards()
    story_points = board.calculate_story_points()

    # Display and adjust story points
    show_sp_calculations(story_points)
    story_points = prompt_for_manual_corrections(story_points)

    # Compute recommendation
    recommendation = compute_recommendation(
        board, story_points, sprint_controls)

    # Insert sprint summary data into the database
    insert_sprint_summary(
        sprint_db_manager,
        board_config['board_id'],
        sprint_controls,
        story_points)

    # Print final results
    print("\nFINAL RESULTS:")
    show_sp_calculations(story_points, recommendation)

    # Optionally save board data to database
    if prompt_for_board_insert() == 0:
        board_data = {
            'board_id': board_config['board_id'],
            'board_name': 'SPRINT-Now Board',
            'json_data': json.dumps(board.get_data())
        }
        sprint_db_manager.insert_data('boards', board_data)


def get_board_data(sprint_db_manager, trello_api, board_source):
    """
    Retrieve board data either from the database or from the live Trello board.

    Args:
        sprint_db_manager (SprintDBManager): The database manager instance.
        trello_api (TrelloAPI): The Trello API instance.
        board_source (int): Indicator of the source of the board data (0 for DB, else live board).

    Returns:
        dict: The board data in JSON format.
    """
    board_data = None
    if board_source == 0:
        # Fetch available boards from the database
        boards = sprint_db_manager.execute_query(
            query="SELECT id, board_name, created_at FROM boards;",
            dic=True
        )
        if not boards:
            print("There are no boards currently in the database...")
        else:
            # Display available boards
            for entry in boards:
                print(
                    ', '.join(
                        f"{key}: {value}" for key,
                        value in entry.items()))
            # Prompt user to select a board
            user_board_id = validate_user_input(
                input("Please enter the ID of the old board you'd like to load: "))
            try:
                # Attempt to retrieve board data from the database
                board_data = sprint_db_manager.get_board_data_from_db(
                    assigned_board_id=user_board_id
                )
            except Exception as e:
                print(f"Error: {e}\nPulling data from live board...")
    if board_data is None:
        # Fetch board data from the live Trello board
        board_data = trello_api.get_board_cards()
    return board_data


def compute_recommendation(board, story_points, sprint_controls):
    """
    Compute the recommended number of story points for the next sprint.

    Args:
        board (Board): The Board instance containing card data.
        story_points (dict): Dictionary containing calculated story points.
        sprint_controls (dict): Dictionary containing sprint control data.

    Returns:
        int: The recommended number of story points.
    """
    # Calculate average unplanned and retro leftover points from the past six
    # sprints
    avg_unplanned = statistics.median(board.get_unplanned_past_sprints()[-6:])
    avg_retro_leftover = statistics.median(board.get_retro_past_sprints()[-6:])

    # Adjustments based on sprint length and team availability
    length_adjustment = sprint_controls['last_sprint_days'] / \
        sprint_controls['next_sprint_days']
    pto_adjustment = (
        sprint_controls['missed_next_sprint'] -
        sprint_controls['missed_last_sprint']
    ) / sprint_controls['members']

    # Calculate the recommendation
    recommendation = math.ceil(
        (
            story_points['planned']['spent']
            + story_points['unplanned']['spent']
            + story_points['retro']['spent']
            - avg_unplanned
            - avg_retro_leftover
        )
        / length_adjustment
        - pto_adjustment
    )
    return recommendation


def insert_sprint_summary(sprint_db_manager, board_id,
                          sprint_controls, story_points):
    """
    Insert the sprint summary data into the database.

    Args:
        sprint_db_manager (SprintDBManager): The database manager instance.
        board_id (str): The ID of the Trello board.
        sprint_controls (dict): Dictionary containing sprint control data.
        story_points (dict): Dictionary containing calculated story points.
    """
    # Prepare sprint summary data
    sprint_summary_data = {
        'board_id': board_id,
        'start_date': date.today().strftime('%Y-%m-%d'),
        'length_days': sprint_controls['last_sprint_days'],
        'members': sprint_controls['members'],
        'vacation_days': sprint_controls['missed_last_sprint'],
        'planned_total': story_points['planned']['total'],
        'planned_completed': story_points['planned']['spent'],
        'planned_remaining': story_points['planned']['remaining'],
        'unplanned_total': story_points['unplanned']['total'],
        'unplanned_completed': story_points['unplanned']['spent'],
        'unplanned_remaining': story_points['unplanned']['remaining'],
        'retro_total': story_points['retro']['total'],
        'retro_completed': story_points['retro']['spent'],
        'retro_remaining': story_points['retro']['remaining'],
    }
    # Insert data into the 'sprint_summary' table
    sprint_db_manager.insert_data('sprint_summary', sprint_summary_data)


if __name__ == "__main__":
    main()
