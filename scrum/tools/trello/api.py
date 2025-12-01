"""
api.py

This module contains the `TrelloAPI` class, which handles interactions with the Trello API,
including fetching board and card data, retrieving story points, and deleting cards.

Classes:
	- TrelloAPI: Manages API requests to Trello.
"""

import re
import requests
import json

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

	def put_call(self, card_id, custom_field_id, value):
		"""Makes a PUT request to update a custom_field_id on a card

		Args:
			card_id (str): ID of the target card
			custom_field_id (str): ID of the target custom field
			value (int): value to push to the custom field
		"""
		# Define api endpoint to update custom field on the given card
		url = f"https://api.trello.com/1/cards/{card_id}/customField/{custom_field_id}/item"
		# Set connection parameters
		headers = {
			"Content-Type": "application/json"
		}
		query = {
			'key': self.api_key,
			'token': self.api_token
		}
		payload = json.dumps({
			"value": {
				"number": str(value)
			}
		})
		# Execute request
		response = requests.request(
			"PUT",
			url,
			data=payload,
			headers=headers,
			params=query,
			timeout=60
		)
		# Print reason on http failure
		try:
			response.raise_for_status()
		except:
			print(response.reason)

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

	def get_custom_fields_data(self):
		"""Retrieves the story points (size, spent, remaining) for a given card.

		Returns:
			json: All customField data from the board asigned to this class
		"""
		card_url = f"{self.base_url}/boards/{self.board_id}/cards/?fields=name&customFieldItems=true"
		plugin_data = self.request_call(url=card_url, have_headers=False)
		return plugin_data

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
