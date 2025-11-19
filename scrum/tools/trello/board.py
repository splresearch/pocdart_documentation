"""
board.py

This module contains the `Board` class, which represents a Trello board and includes methods to
fetch board data, extract card information, and calculate story points.

Classes:
	- Board: Represents a Trello board and includes methods for data fetching and calculations.
"""

import re
from pathlib import Path
from trello.card import Card
from sprint_utils import load_config


class Board:
	def __init__(self, api, board_data=None):
		"""
		Initializes a Board instance.

		Args:
			api (TrelloAPI): An instance of the TrelloAPI class.
			board_data (dict, optional): Initial data for the board. 
				If None, data will be fetched using the API.
		"""
		self.api = api
		self.cards = []
		self.unplanned_past_sprints = []
		self.retro_past_sprints = []
		self.calcs = {
			"unplanned": {"total": 0, "spent": 0, "remaining": 0},
			"planned": {"total": 0, "spent": 0, "remaining": 0},
			"retro": {"total": 0, "spent": 0, "remaining": 0},
		}
		self.lists = api.get_board_lists()
		if board_data is None:
			self.fetch_data()
		else:
			self.board_data = board_data

		# Load board configuration
		board_config = load_config(
			Path(__file__).parent.parent /
			"config.json")['board']
		self.unplanned_template_card = board_config['unplanned_template_card']
		self.sprint_summary_card = board_config['sprint_calc_card']
		self.sp_total_id = board_config['sp_total_id']
		self.sp_spent_id = board_config['sp_spent_id']

	def get_data(self):
		"""
		Returns the board data.

		Returns:
			dict: The board data.
		"""
		return self.board_data

	def get_cards(self):
		"""
		Returns the list of Card objects.

		Returns:
			list: A list of Card instances.
		"""
		return self.cards

	def get_unplanned_past_sprints(self):
		"""
		Returns the unplanned story points from past sprints.

		Returns:
			list: A list of integers representing unplanned story points.
		"""
		return self.unplanned_past_sprints

	def get_retro_past_sprints(self):
		"""
		Returns the retro story points from past sprints.

		Returns:
			list: A list of integers representing retro story points.
		"""
		return self.retro_past_sprints

	def fetch_data(self):
		"""
		Fetches board data from the Trello API and sets the board_data attribute.
		"""
		self.board_data = self.api.get_board_cards()

	def extract_cards(self, calc_sp = True):
		"""
		Extracts card data from the board's JSON data and creates Card objects.

		Args:
			calc_sp (bool): should story points be calculated for each card
		"""
		# Preprocess list IDs to names for quick lookup
		list_id_to_name = {list_obj['id']: list_obj['name']
						   for list_obj in self.lists}

		# Compile regex patterns once to improve performance
		unplanned_pattern = re.compile(r"SP Unplanned:\s*(\d+)\(T\)", re.IGNORECASE)
		retro_pattern = re.compile(r"SP Retro:\s*(\d+)\(T\)", re.IGNORECASE)

		# Get custom field data
		custom_fields_data = self.api.get_custom_fields_data()

		# Iterate board data to parse individual cards into Card() objects
		for card in self.board_data:
			curr_card_id = card.get("id")
			curr_card_short_link = card.get("shortLink")
			curr_card_name = card.get("name", "")
			curr_card_labels = [
				label.get(
					"name",
					"") for label in card.get(
					"labels",
					[])]
			curr_card_list = list_id_to_name.get(card.get('idList'), '')

			# Skip if card is in 'Monitoring' list
			if "Monitoring" in curr_card_list:
				continue

			# Skip the unplanned template card
			if curr_card_id == self.unplanned_template_card:
				continue

			# Process the sprint summary card
			if curr_card_id == self.sprint_summary_card:
				desc = card.get("desc", "")
				self.unplanned_past_sprints = [
					int(i) for i in unplanned_pattern.findall(desc)]
				self.retro_past_sprints = [
					int(i) for i in retro_pattern.findall(desc)]
				continue

			# Extract story points
			if calc_sp:
				story_points = self.api.get_card_story_points(curr_card_name, curr_card_id)
			else:
				story_points = {
					"total": 0,
					"spent": 0,
					"remaining": 0
				}

			# Create and append the Card object
			self.cards.append(
				Card(
					card_id=curr_card_id,
					short_link=curr_card_short_link,
					story_points=story_points,
					title=curr_card_name,
					labels=curr_card_labels,
					list_name=curr_card_list
				)
			)

	def parse_story_points(self, card_id, custom_fields_data):
		story_points = {
			"total": 0,
			"spent": 0,
			"remaining": 0
		}
		for card in custom_fields_data:
			if card["id"] == card_id:
				for field in card["customFieldItems"]:
					if field["id"] == self.sp_total_id:
						story_points["total"] = int(field["value"]["number"])
					elif field["id"] == self.sp_spent_id:
						story_points["spent"] = int(field["value"]["number"])
				remaining = story_points["total"] - story_points["spent"]
				story_points["remaining"] = remaining if remaining >= 0 else 0
				return story_points

	def calculate_story_points(self):
		"""
		Calculates story points for the board.

		Returns:
			dict: A dictionary with calculated story points for 
				'planned', 'unplanned', and 'retro' categories.
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
