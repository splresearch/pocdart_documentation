"""
api.py

This module contains the TrelloAPI class, which handles interactions with the Trello API,
including fetching board and card data.

Classes:
    - TrelloAPI: Manages API requests to Trello.

Example:
"""

import requests, json, os, sys, re

class TrelloAPI:
    def __init__(self, board_id, api_key, api_token):
        self.board_id = board_id
        self.api_key = api_key
        self.api_token = api_token
        self.base_url = "https://api.trello.com/1"

    def request_call(self, url, have_headers):
        """Makes a GET request to the specified board using the requests library.

        Args:
            url: str, the URL to make the GET request to.
            have_headers: bool, specifies if the request should include headers.

        Returns:
            dict, the JSON response from the API.
        """
        if have_headers:
            headers = {
                "Accept": "application/json"
            }
        else:
            headers = {}

        query = {
            'key': self.api_key,
            'token': self.api_token
        }

        response = requests.request(
            "GET",
            url,
            params=query,
            headers=headers,
            timeout=60
        )

        return response.json()

    def get_board_cards(self):
        cards_url = self.base_url + f"/boards/{self.board_id}/cards"
        sprint_cards = self.request_call(url=cards_url, have_headers=False)

        return sprint_cards

    def get_board_lists(self):
        lists_url = self.base_url + f"/boards/{self.board_id}/lists"
        sprint_lists = self.request_call(url=lists_url, have_headers=False)

        return sprint_lists

    def get_card_story_points(self, card_name, card_id):
        card_url = self.base_url + f"/cards/{card_id}/pluginData"
        plugin_data = self.request_call(url=card_url, have_headers=False)

        # If the card size module has not been filled out, set everything to
        # zero
        if not plugin_data:
            print(
                f"This card, {card_name}, has not been estimated, assigned values of 0")
            card_size = {
                "total": 0,
                "spent": 0,
                "remaining": 0
            }
        else:
            # Parse request for card size
            values = re.findall(
                r'"size":(\d+),\s*"spent":(\d+)',
                plugin_data[0]['value'])
            card_size = {
                "total": int(values[0][0]),
                "spent": int(values[0][1]),
                "remaining": int(values[0][0]) - int(values[0][1])
            }

        return card_size

    def delete_card(self, card_id):
        """Makes a DELETE request for the specified card using the requests library.

        Args:
            id: str, 24 character hexadecimal card id (not shortLink)

        Usage:
            # to delete cards older than <date>
            from datetime import datetime
            from dateutil.relativedelta import relativedelta
            # request all closed cards from twilio for target board
            cards_url = f"https://api.trello.com/1/boards/{board_id}/cards?filter=closed&"
            sprint_cards = request_call(url=cards_url, have_headers=False)
            # iterate cards
            for card in sprint_cards:
                # if last activity is older than one year
                if datetime.strptime(card['dateLastActivity'], "%Y-%m-%dT%H:%M:%S.%fZ") <  datetime.today() - relativedelta(years=1):
                    # delete with card id
                    response = delete_card(card['id'])

        Returns:
            delete response from Twilio API
        """
        url = self.base_url + "/cards/" + id

        query = {
            'key': config_var["api_key"],
            'token': config_var["api_token"]
        }
        
        response = requests.request(
        "DELETE",
        url,
        params=query
        )

        return response.text
