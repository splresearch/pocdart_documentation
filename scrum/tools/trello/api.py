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
