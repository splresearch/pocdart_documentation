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
    if card.get_short_link() == 'tAm3ipG3':
        json_object = {
            "idValue": board_config['sp_total_id'],
            "key": '',
            "value": { "number": card.get_total_story_points() }
        }
        url = "https://api.trello.com/1/card/" + card.get_card_id() + "/customField/" + board_config['sp_total_id'] + "/item"
        print(url)
        print(json_object)
        # trello_api.put_call(
        #     url = url
        # )