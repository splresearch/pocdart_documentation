"""
card.py

This module contains the `Card` class, which represents a Trello card and includes methods to
hold and manipulate card data.

Classes:
    - Card: Represents a Trello card and holds card data.
"""


class Card:
    def __init__(
            self,
            card_id,
            story_points,
            title='',
            labels=None,
            list_name=''):
        """
        Initializes a Card instance.

        Args:
            card_id (str): The Trello card ID.
            story_points (dict): The story points of the card, with keys 'total', 'spent', 'remaining'.
            title (str, optional): The title of the card. Defaults to an empty string.
            labels (list, optional): The labels of the card. Defaults to an empty list.
            list_name (str, optional): The name of the list the card is in. Defaults to an empty string.
        """
        self.card_id = card_id
        self.story_points = story_points
        self.title = title
        self.labels = labels if labels is not None else []
        self.list_name = list_name

    # Getters
    def get_card_id(self):
        """
        Returns the card ID.

        Returns:
            str: The card ID.
        """
        return self.card_id

    def get_story_points(self):
        """
        Returns the story points dictionary.

        Returns:
            dict: The story points of the card.
        """
        return self.story_points

    def get_total_story_points(self):
        """
        Returns the total story points assigned to the card.

        Returns:
            int: The total story points.
        """
        return self.story_points.get("total", 0)

    def get_spent_story_points(self):
        """
        Returns the spent story points for the card.

        Returns:
            int: The spent story points.
        """
        return self.story_points.get("spent", 0)

    def get_remaining_story_points(self):
        """
        Returns the remaining story points for the card.

        Returns:
            int: The remaining story points.
        """
        return self.story_points.get("remaining", 0)

    def get_title(self):
        """
        Returns the title of the card.

        Returns:
            str: The card title.
        """
        return self.title

    def get_labels(self):
        """
        Returns the labels attached to the card.

        Returns:
            list: A list of label names.
        """
        return self.labels

    def get_list_name(self):
        """
        Returns the name of the list the card is in.

        Returns:
            str: The list name.
        """
        return self.list_name

    # Setters
    def set_card_id(self, card_id):
        """
        Sets the card ID.

        Args:
            card_id (str): The new card ID.
        """
        self.card_id = card_id

    def set_story_points(self, story_points):
        """
        Sets the story points dictionary.

        Args:
            story_points (dict): The new story points dictionary.
        """
        self.story_points = story_points

    def set_total_story_points(self, total_points):
        """
        Sets the total story points for the card.

        Args:
            total_points (int): The total story points.
        """
        self.story_points["total"] = total_points

    def set_spent_story_points(self, spent_points):
        """
        Sets the spent story points for the card.

        Args:
            spent_points (int): The spent story points.
        """
        self.story_points["spent"] = spent_points

    def set_remaining_story_points(self, remaining_points):
        """
        Sets the remaining story points for the card.

        Args:
            remaining_points (int): The remaining story points.
        """
        self.story_points["remaining"] = remaining_points

    def set_title(self, title):
        """
        Sets the title of the card.

        Args:
            title (str): The new title.
        """
        self.title = title

    def set_labels(self, labels):
        """
        Sets the labels for the card.

        Args:
            labels (list): A list of label names.
        """
        self.labels = labels

    def set_list_name(self, list_name):
        """
        Sets the name of the list the card is in.

        Args:
            list_name (str): The new list name.
        """
        self.list_name = list_name
