"""
test_api.py

This module contains unit tests for the TrelloAPI class, ensuring that the API interactions
with Trello are correctly implemented.

Tests:
	- test_get_board_cards: Tests the get_board_cards method.
	- test_get_board_lists: Tests the get_board_lists method.
	- test_get_card_story_points: Tests the get_card_story_points method.
"""

import sys
from pathlib import Path
import pytest

# Add the parent directory to the Python path
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))

from trello.api import TrelloAPI
from sprint_utils import load_config


@pytest.fixture(scope='module')
def board_config():
	"""
	Fixture to load the board configuration.

	Returns:
		dict: The board configuration dictionary.
	"""
	return load_config(parent_path / "config.json")['board']


@pytest.fixture(scope='module')
def trello_api(board_config):
	"""
	Fixture to create a TrelloAPI instance for testing.

	Args:
		board_config (dict): The board configuration fixture.

	Returns:
		TrelloAPI: An instance of the TrelloAPI class.
	"""
	# Initialize TrelloAPI instance
	api = TrelloAPI(
		board_id=board_config['board_id'],
		api_key=board_config['api_key'],
		api_token=board_config['api_token']
	)
	return api


def test_get_board_cards(trello_api, board_config):
	"""
	Tests the get_board_cards method of the TrelloAPI class.

	Args:
		trello_api (TrelloAPI): The TrelloAPI instance fixture.
		board_config (dict): The board configuration fixture.
	"""
	# Act: Call get_board_cards method
	sprint_cards = trello_api.get_board_cards()

	# Assert: Verify that the response data matches expected values
	assert sprint_cards is not None
	assert len(sprint_cards) > 0
	# Assuming 'sprint_calc_card' is expected to be in the list of cards
	card_ids = [card['id'] for card in sprint_cards]
	assert board_config['sprint_calc_card'] in card_ids


def test_get_board_lists(trello_api):
	"""
	Tests the get_board_lists method of the TrelloAPI class.

	Args:
		trello_api (TrelloAPI): The TrelloAPI instance fixture.
	"""
	# Act: Call get_board_lists method
	sprint_lists = trello_api.get_board_lists()

	# Assert: Verify that the response data matches expected values
	assert sprint_lists is not None
	assert len(sprint_lists) > 0

def test_get_custom_fields_data(trello_api):
	"""
	Tests the get_custom_fields_data method of the TrelloAPI class.

	Args:
		trello_api (TrelloAPI): The TrelloAPI instance fixture.
	"""
	# Act: Call get_board_lists method
	custom_fields_data = trello_api.get_custom_fields_data()

	# Assert: Verify that the response data matches expected values
	assert custom_fields_data is not None
	assert len(custom_fields_data) > 0
	assert 'customFieldItems' in custom_fields_data[0].keys()

	# Assert at least one populated card has a parsable integer
	card_field_data = [x['customFieldItems'] for x in custom_fields_data if len(x['customFieldItems']) > 0][0]
	assert isinstance(int(card_field_data[0]['value']['number']), int)
