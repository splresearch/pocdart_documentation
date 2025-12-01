""" Convert a Trello card ID to the associated shortLink """

## Get SP from current system
import os, sys
os.chdir("/home/pocdart/pocdart_documentation/scrum/tools/")
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# Import local modules
from sprint_utils import load_config
from trello.api import TrelloAPI
from trello.board import Board

def main(card_id):
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
    board.extract_cards(calc_sp = False)
    # Print results to console
    print([card.get_short_link() for card in board.get_cards() if card.get_card_id() == card_id])

if __name__ == "__main__":
    card_id = sys.argv[1]
    main(card_id)