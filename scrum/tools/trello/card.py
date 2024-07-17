"""
card.py

This module contains the Card class, which represents a Trello card and includes methods to
hold card data.

Classes:
    - Card: Represents a Trello card and holds card data.
"""

class Card:
    def __init__(self, card_id, story_points, title='', labels=None, list_name=''):
        """
        Initializes a Card instance.

        Args:
            card_id (str): The Trello card ID.
            story_points (dict): The story points of the card.
            title (str): The title of the card.
            labels (list): The labels of the card.
            list_name (str): The name of the list the card is in.
        """
        self.card_id = card_id
        self.story_points = story_points
        self.title = title
        self.labels = labels if labels is not None else []
        self.list_name = list_name

    # Getters
    def get_card_id(self):
        return self.card_id

    def get_story_points(self):
        return self.story_points

    def get_title(self):
        return self.title

    def get_labels(self):
        return self.labels

    def get_list_name(self):
        return self.list_name

    # Setters
    def set_card_id(self, card_id):
        self.card_id = card_id

    def set_story_points(self, story_points):
        self.story_points = story_points

    def set_title(self, title):
        self.title = title

    def set_labels(self, labels):
        self.labels = labels

    def set_list_name(self, list_name):
        self.list_name = list_name
