"""
api.py

This module contains the `TrelloAPI` class, which handles interactions with the Trello API,
including fetching board and card data, retrieving story points, and deleting cards.

Classes:
    - TrelloAPI: Manages API requests to Trello.

Example:
    trello_api = TrelloAPI(board_id='your_board_id', api_key='your_api_key', api_token='your_api_token')
    cards = trello_api.get_board_cards()
    lists = trello_api.get_board_lists()
    card_story_points = trello_api.get_card_story_points(card_name='Card Name', card_id='Card ID')
    delete_response = trello_api.delete_card(card_id='Card ID')
"""

import requests
import re

class TrelloAPI:
    def __init__(self, board_id, api_key, api_token):
        """
        Initializes the TrelloAPI instance with board credentials.

        Args:
            board_id (str): The ID of the Trello board.
            api_key (str): Your Trello API key.
            api_token (str): Your Trello API token.
        """
        self.board_id = board_id
        self.api_key = api_key
        self.api_token = api_token
        self.base_url = "https://api.trello.com/1"

    def request_call(self, url, have_headers):
        """Makes a GET request to the specified URL using the requests library.

        Args:
            url (str): The URL to make the GET request to.
            have_headers (bool): Specifies if the request should include headers.

        Returns:
            dict or list: The JSON response from the API.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        headers = {"Accept": "application/json"} if have_headers else {}
        query = {
            'key': self.api_key,
            'token': self.api_token
        }

        response = requests.get(
            url,
            params=query,
            headers=headers,
            timeout=60
        )
        response.raise_for_status()
        return response.json()

    def get_board_cards(self):
        """Retrieves all cards from the Trello board.

        Returns:
            list: A list of card dictionaries from the board.
        """
        cards_url = f"{self.base_url}/boards/{self.board_id}/cards"
        sprint_cards = self.request_call(url=cards_url, have_headers=False)
        return sprint_cards

    def get_board_lists(self):
        """Retrieves all lists from the Trello board.

        Returns:
            list: A list of list dictionaries from the board.
        """
        lists_url = f"{self.base_url}/boards/{self.board_id}/lists"
        sprint_lists = self.request_call(url=lists_url, have_headers=False)
        return sprint_lists

    def get_card_story_points(self, card_name, card_id):
        """Retrieves the story points (size, spent, remaining) for a given card.

        Args:
            card_name (str): The name of the card.
            card_id (str): The ID of the card.

        Returns:
            dict: A dictionary with 'total', 'spent', and 'remaining' story points.
        """
        card_url = f"{self.base_url}/cards/{card_id}/pluginData"
        plugin_data = self.request_call(url=card_url, have_headers=False)

        # If the card size module has not been filled out, set everything to zero
        if not plugin_data:
            print(f"This card, '{card_name}', has not been estimated. Assigned values of 0.")
            card_size = {
                "total": 0,
                "spent": 0,
                "remaining": 0
            }
        else:
            # Parse plugin data for card size
            match = re.search(
                r'"size":(\d+),\s*"spent":(\d+)',
                plugin_data[0]['value']
            )
            if match:
                total = int(match.group(1))
                spent = int(match.group(2))
                remaining = max(total - spent, 0)
                card_size = {
                    "total": total,
                    "spent": spent,
                    "remaining": remaining
                }
            else:
                print(f"Could not parse story points for card '{card_name}'. Assigned values of 0.")
                card_size = {
                    "total": 0,
                    "spent": 0,
                    "remaining": 0
                }

        return card_size

    def delete_card(self, card_id):
        """Deletes a card from the Trello board.

        Args:
            card_id (str): The 24-character hexadecimal ID of the card (not shortLink).

        Returns:
            str: The response text from the Trello API.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.

        Example:
            delete_response = trello_api.delete_card(card_id='Card ID')
            print(delete_response)
        """
        url = f"{self.base_url}/cards/{card_id}"
        query = {
            'key': self.api_key,
            'token': self.api_token
        }
        response = requests.delete(url, params=query, timeout=60)
        response.raise_for_status()
        return response.text