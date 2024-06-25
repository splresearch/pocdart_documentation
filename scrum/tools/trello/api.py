"""
api.py

This module contains the TrelloAPI class, which handles interactions with the Trello API,
including fetching board and card data.

Classes:
    - TrelloAPI: Manages API requests to Trello.

Example:
"""

import requests

class TrelloAPI:
    def __init__(self, api_key, token):
        self.api_key = api_key
        self.token = token
        self.base_url = "https://api.trello.com/1"

    def request_call(self, url, have_headers):
        pass

    def get_board_cards(self, board_id):
        pass

    def get_board_lists(self, board_id):
        pass

    def get_card_story_points(self, card_id):
        pass
