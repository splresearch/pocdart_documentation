"""
board.py

This module contains the Board class, which represents a Trello board and includes methods to
fetch board data and calculate story points.

Classes:
    - Board: Represents a Trello board and includes methods for data fetching and calculation.
"""

import requests

class Board:
    def __init__(self, board_id, api, data):
        """
        Initializes a Board instance.

        Args:
            board_id (str): The Trello board ID.
            api (TrelloAPI): An instance of the TrelloAPI class.
            data (dict): Initial data for the board.
        """
        self.board_id = board_id
        self.api = api
        self.data = data

    def fetch_data(self):
        """
        Fetches board data from the Trello API and sets the data attribute.
        """
        pass

    def extract_cards(self):
        """
        Extracts card data from the board's JSON data and creates Card objects.
        """
        pass

    def calculate_story_points(self):
        """
        Calculates story points for the board.

        Returns:
            dict: A dictionary with calculated story points for planned, unplanned, and retro categories.
        """
        pass
