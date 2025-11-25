## Get SP from current system
import os, sys, pprint
from colorama import Fore, Back, Style
os.chdir("/home/pocdart/pocdart_documentation/scrum/tools/")
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

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

# By label
# Initialize story point totals
sp_total_internal_work = 0
sp_total_feature = 0
# Iterate cards
for card in board.get_cards():
    # Count internal work
    if "Internal Work" in card.get_labels():
        sp_total_internal_work += card.get_total_story_points()
    # Count all other planned work against it (i.e. User Story + Change)
    elif "UNPLANNED" not in card.get_labels():
        sp_total_feature += card.get_total_story_points()
# Calculate ratio of internal work to all work
iw_ratio = sp_total_internal_work / (sp_total_internal_work + sp_total_feature)
# Convert to percentage
iw_percentage = round(iw_ratio * 100, 0)
# Print result to console

if iw_percentage > 50:
    iw_color = Fore.RED
elif iw_percentage > 40:
    iw_color = Fore.YELLOW
else:
    iw_color = Fore.GREEN

print("Internal work percentage: " + iw_color + str(iw_percentage) + "%")
print(Style.RESET_ALL)

# By owner
# Initialize result object
sp_by_owner = {}
# Define owner id-name mapping
owner_lookup = {
    '4f19bc8abb8de80d1c02ef62': 'Andrew',
    '62b5e317e63365744d39d516': 'Allen',
    '56f2b2493ac46542079684d0': 'AlexM',
    '5d24c03c4813671044432ba3': 'Amber',
    '5f03985091b8f77fba676276': 'Lucy',
    '59f20e80fbe83676bd4594c9': 'Matt',
    '61294506a476ee89c9d40c90': 'Duncan',
    '63866dafc7317a03d5b0c08d': 'Jacqui',
    '596526123b40082ebe745014': 'AlexK',
    '664cb827f86bb7b271fe12f8': 'Hazel',
    '677d9db991fcc949febc2b53': 'Nick',
    '551d9dde6f41314e814727c0': 'Robert',
    '572778f2ff1f780105746ff0': 'Emily'
}
# Iterate cards
for card in board.get_cards():
    # Extract members
    idMembers = card.get_idMembers()
    # If members exist
    if len(idMembers) > 0:
        # Use mapping to get name of first idMember listed
        name = owner_lookup[idMembers[0]]
        # If first card for this name, add
        if name not in sp_by_owner.keys():
            sp_by_owner[name] = card.get_total_story_points()
        # Else increment
        else:
            sp_by_owner[name] += card.get_total_story_points()
# Reverse sort
sorted = dict(sorted(sp_by_owner.items(), key=lambda item: item[1], reverse = True))
# Print result to console
print("Story points by owner:")
pprint.pp(sorted)
# Get list of owners with zero points or not listed
no_points = [k for k,v in sp_by_owner.items() if v == 0] + [y for x,y in owner_lookup.items() if y not in sp_by_owner.keys()]
no_points.sort()
# Print result to console
print('Members with zero story points assigned: ' + ', '.join(no_points))

