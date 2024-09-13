"""
board.py

This module contains the Board class, which represents a Trello board and includes methods to
fetch board data and calculate story points.

Classes:
    - Board: Represents a Trello board and includes methods for data fetching and calculation.
"""

import requests, os, sys, re

# Get the absolute path of the 'utils' directory relative to this file's location
parent_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))

# Add the parent directory to the Python path
sys.path.append(parent_path)
from sprint_utlis import load_config
from trello.card import Card

class Board:
    def __init__(self, api, board_data = None):
        """
        Initializes a Board instance.

        Args:
            api (TrelloAPI): An instance of the TrelloAPI class.
            board_data (dict): Initial data for the board. Can be None if wanting to pull from API rather than DB
        """
        self.api = api
        self.cards = []
        self.unplanned_past_sprints = None
        self.retro_past_sprints = None
        self.calcs = {
            "unplanned": {
                "total": 0,
                "spent": 0,
                "remaining": 0
            },
            "planned": {
                "total": 0,
                "spent": 0,
                "remaining": 0
            },
            "retro": {
                "total": 0,
                "spent": 0,
                "remaining": 0
            }
        }
        self.lists = api.get_board_lists()
        if board_data is None:
            self.fetch_data()
        else:
            self.board_data = board_data

        board_config = load_config("../config.json")['board']
        self.unplanned_template_card = board_config['unplanned_template_card']
        self.sprint_summary_card = board_config['sprint_calc_card']

    def get_data(self):
        return self.board_data
    def get_cards(self):
        return self.cards

    def fetch_data(self):
        """
        Fetches board data from the Trello API and sets the data attribute.
        """
        self.board_data = self.api.get_board_cards()

    def extract_cards(self):
        """
        Extracts card data from the board's JSON data and creates Card objects.
        """
        for card in self.board_data:
            curr_card_id = card["id"]
            curr_card_name = card["name"]
            curr_card_labels = [subitem["name"] for subitem in card["labels"]]
            curr_card_list = next(
                list_obj for list_obj in self.lists if list_obj["id"] in card['idList'])["name"]
            if (curr_card_id == self.unplanned_template_card or
                "Monitoring" in curr_card_list):
                continue
            # If the card is the Sprint calc history card,
            #   pull out all the unplanned story points from previous Sprints
            if curr_card_id == self.sprint_summary_card:
                self.unplanned_past_sprints = re.findall(
                    r"unplanned: \*{2}(\d+)", card["desc"], re.IGNORECASE)
                self.unplanned_past_sprints = [int(i) for i in self.unplanned_past_sprints]
                self.retro_past_sprints = re.findall(
                    r"\\\*\\\* (\d+)\\\*\\\* Retro", card["desc"], re.IGNORECASE)
                self.retro_past_sprints = [int(i) for i in self.retro_past_sprints]
                continue
            self.cards.append(
                Card(
                    card_id = curr_card_id,
                    story_points = self.api.get_card_story_points(curr_card_name, curr_card_id),
                    title = curr_card_name,
                    labels = curr_card_labels,
                    list_name = curr_card_list
                )
            )

    def calculate_story_points(self):
        """
        Calculates story points for the board.

        Returns:
            dict: A dictionary with calculated story points for planned, unplanned, and retro categories.
        """
        for card in self.cards:
            # Handle if in monitoring
            if "Monitoring" in card.get_list_name():
                continue

            # Handle if unplanned
            if "UNPLANNED" in card.get_list_name():
                self.calcs['unplanned']['total'] += card.get_total_story_points()

            # Handle if in done list
            if "Done" in card.get_list_name():
                self.calcs['planned']['total'] += card.get_total_story_points()
                self.calcs['planned']['spent'] += card.get_total_story_points()
                # If extra work was spent on card, add to Retro completed
                if new_card.size["spent"] > new_card.size["size"]:
                    SP_RETRO_COMPLETED = SP_RETRO_COMPLETED + \
                        (new_card.size["spent"] - new_card.size["size"])

            # Handle if still on other parts of the board
            if "Done" not in new_card.list_name:
                # If unplanned
                if "UNPLANNED" in new_card.labels:
                    if new_card.size["spent"] > 0:
                        SP_UNPLANNED_PARTIAL_COMPLETED += new_card.size["spent"]
                    elif new_card.size["spent"] == 0:
                        SP_UNPLANNED_REMAINING += new_card.size["remaining"]
                # If Retro
                elif "RETRO" in new_card.labels:
                    SP_RETRO_LEFTOVER += new_card.size["remaining"]
                # Otherwise, incomplete card must be counted
                elif new_card.size["spent"] > 0:
                    # Capture any story point overflow with retro completed
                    if new_card.size["spent"] > new_card.size["size"]:
                        SP_RETRO_COMPLETED = SP_RETRO_COMPLETED + \
                            (new_card.size["spent"] - new_card.size["size"])
                        SP_PLANNED_PARTIAL_COMPLETED += new_card.size["size"]
                    # Capture fully spent cards with no extra spent points above size
                    elif new_card.size["spent"] == new_card.size["size"]:
                        SP_PLANNED_PARTIAL_COMPLETED += new_card.size["size"]
                    # Capture actual partial completed cards
                    else:
                        SP_PLANNED_PARTIAL_COMPLETED += new_card.size['spent']
