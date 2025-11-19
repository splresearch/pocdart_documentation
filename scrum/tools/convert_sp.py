## Get SP from current system
import os
os.chdir("/home/pocdart/pocdart_documentation/scrum/tools/")
# Import local modules
from sprint_utils import load_config
from trello.api import TrelloAPI
from trello.board import Board

# Load configuration
board_config = load_config("config.json")['board']
# Initialize database manager and Trello API
trello_api = TrelloAPI(
    board_id=board_config['board_id'],
    api_key=board_config['api_key'],
        api_token=board_config['api_token']
)
# Get board data
board_data = trello_api.get_board_cards()
board = Board(trello_api, board_data)
board.extract_cards(calc_sp = True)

## Convert (double, round to fib)
for card in board.get_cards():
    trello_api.put_call(
        card.get_card_id(),
        board_config['sp_total_id'],
        card.get_total_story_points()
    )
    trello_api.put_call(
        card.get_card_id(),
        board_config['sp_spent_id'],
        card.get_spent_story_points()
    )
