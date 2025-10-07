import statistics
import math
import json
from datetime import date
import os

os.chdir('/home/pocdart/pocdart_documentation/scrum/tools/')

from trello.db import SprintDBManager
from trello.api import TrelloAPI
from trello.board import Board
from sprint_utils import load_config

# Load configuration
config = load_config("config.json")
mysql_config = config['mysql']
board_config = config['board']

# Initialize database manager and Trello API
sprint_db_manager = SprintDBManager(mysql_config)
trello_api = TrelloAPI(
    board_id=board_config['board_id'],
    api_key=board_config['api_key'],
    api_token=board_config['api_token']
)

# Get board data
board_data = trello_api.get_board_cards()
board = Board(trello_api, board_data)
board.extract_cards(calc_sp = False)
cards = board.get_cards()
card_links = []
for card in cards:
    card_links += [card.get_short_link()]

output = '|'.join(card_links)
print(output)