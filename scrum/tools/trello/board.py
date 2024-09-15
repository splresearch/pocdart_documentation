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
        # Preprocess list IDs to names for quick lookup
        list_id_to_name = {list_obj['id']: list_obj['name'] for list_obj in self.lists}

        # Compile regex patterns once to improve performance
        unplanned_pattern = re.compile(r"unplanned: \*{2}(\d+)", re.IGNORECASE)
        retro_pattern = re.compile(r"\*\* (\d+)\*\* Retro", re.IGNORECASE)

        for card in self.board_data:
            curr_card_id = card.get("id")
            curr_card_name = card.get("name", "")
            curr_card_labels = [label.get("name", "") for label in card.get("labels", [])]
            curr_card_list = list_id_to_name.get(card.get('idList'))

            # Skip if card is in 'Monitoring' list
            if "Monitoring" in curr_card_list:
                continue

            # Skip the unplanned template card
            if curr_card_id == self.unplanned_template_card:
                continue

            # Process the sprint summary card
            if curr_card_id == self.sprint_summary_card:
                self.unplanned_past_sprints = [int(i) for i in unplanned_pattern.findall(card.get("desc", ""))]
                self.retro_past_sprints = [int(i) for i in retro_pattern.findall(card.get("desc", ""))]
                continue

            # Extract story points
            story_points = self.api.get_card_story_points(curr_card_name, curr_card_id)

            # Create and append the Card object
            self.cards.append(
                Card(
                    card_id=curr_card_id,
                    story_points=story_points,
                    title=curr_card_name,
                    labels=curr_card_labels,
                    list_name=curr_card_list
                )
            )

    def calculate_story_points(self):
        """
        Calculates story points for the board.

        Returns:
            dict: A dictionary with calculated story points for planned, unplanned, and retro categories.
        """
        for card in self.cards:
            labels = set(card.get_labels())
            list_name = card.get_list_name()

            is_unplanned = 'UNPLANNED' in labels
            is_retro = 'RETRO' in labels
            is_done = 'Done' in list_name

            total_points = card.get_total_story_points()
            spent_points = card.get_spent_story_points()
            remaining_points = card.get_remaining_story_points()

            # Determine category
            if is_unplanned:
                category = 'unplanned'
            # RETRO is treated as planned if not in DONE and has had some work done to it already
            elif is_retro and not (is_done or spent_points > 0):
                category = 'retro'
            else:
                category = 'planned'

            # Update total points
            self.calcs[category]['total'] += total_points

            # Calculate actual spent and extra spent points
            if category in ('planned', 'unplanned'):
                actual_spent = min(spent_points, total_points)
                extra_spent = max(spent_points - total_points, 0)
                self.calcs[category]['spent'] += actual_spent
                self.calcs['retro']['spent'] += extra_spent
                self.calcs['retro']['total'] += extra_spent
            else:
                self.calcs[category]['spent'] += spent_points

            # Update remaining points if card is not done
            if not is_done:
                self.calcs[category]['remaining'] += remaining_points

        return self.calcs
