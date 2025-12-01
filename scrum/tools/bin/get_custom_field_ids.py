## Get SP from current system
import os, sys, pprint
os.chdir("/home/pocdart/pocdart_documentation/scrum/tools/")
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# Import local modules
from sprint_utils import load_config
from trello.api import TrelloAPI

# Load configuration
board_config = load_config("config.json")['board']
# Initialize database manager and Trello API
trello_api = TrelloAPI(
	board_id=board_config['board_id'],
	api_key=board_config['api_key'],
		api_token=board_config['api_token']
)

custom_fields_data = trello_api.get_custom_fields_data()
populated_custom_fields = [x for x in custom_fields_data if len(x['customFieldItems']) > 0]
pprint.pp(populated_custom_fields[0])