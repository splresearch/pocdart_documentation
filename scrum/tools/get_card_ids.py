""" Print a pipe-deliimeted list of card short_links for all cards on the board """
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
board.extract_cards(calc_sp = False)
# Compile list of short_links
card_links = []
for card in board.get_cards():
	card_links += [card.get_short_link()]
# Format and print output
output = '|'.join(card_links)
print(output)
