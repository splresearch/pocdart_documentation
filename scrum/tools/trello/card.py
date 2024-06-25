"""
card.py

This module contains the Card class, which represents a Trello card and includes methods
to extract and manage story points from the card data.

Classes:
    - Card: Represents a Trello card with attributes and methods to manage story points.

Example:
"""

import json

class Card:
    """
    A class to represent a Trello card.

    Attributes:
        id (str): The unique identifier of the card.
        name (str): The name of the card.
        points (int or None): The story points extracted from the card name.

    Methods:
        extract_story_points(card_data): Extracts story points from the card name.
    """

    def __init__(self, card_data):
        """
        Initializes the Card with card data.

        Args:
            card_data (json): JSON containing the card's data.
        """
        pass

    def extract_id(self):
        pass
    
    def extract_name(self):
        pass

    def extract_labels(self):
        pass

    def extract_list_id(self):
        pass

    def fetch_story_points(self):
        pass
