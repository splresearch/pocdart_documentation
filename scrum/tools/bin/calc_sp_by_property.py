## Get SP from current system
import os, sys, pprint
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
sp_total_internal_work = 0
sp_total_feature = 0
for card in board.get_cards():
    if "Internal Work" in card.get_labels():
        sp_total_internal_work += card.get_total_story_points()
    elif "UNPLANNED" not in card.get_labels():
        sp_total_feature += card.get_total_story_points()
iw_ratio = sp_total_internal_work / (sp_total_internal_work + sp_total_feature)
iw_percentage = round(iw_ratio * 100, 0)
print("Internal work percentage: " + str(iw_percentage) + "%")
# By owner
sp_by_owner = {}
owner_lookup = {
    '4f19bc8abb8de80d1c02ef62': 'Andrew',
    '62b5e317e63365744d39d516': 'Allen',
    '56f2b2493ac46542079684d0': 'AlexM',
    '5d24c03c4813671044432ba3': 'Amber',
    '5f03985091b8f77fba676276': 'Lucy',
    '59f20e80fbe83676bd4594c9': 'Matt',
    '61294506a476ee89c9d40c90': 'Duncan',
    '63866dafc7317a03d5b0c08d': 'Jacqui'
}
for card in board.get_cards():
    idMembers = card.get_idMembers()
    print(idMembers)
    print(card.get_short_link())

    if len(idMembers) > 0:
        name = owner_lookup[idMembers[0]]
        if name not in sp_by_owner.keys():
            sp_by_owner[name] = card.get_total_story_points()
        else:
            sp_by_owner[name] += card.get_total_story_points()
sorted = dict(sorted(sp_by_owner.items(), key=lambda item: item[1], reverse = True))
pprint.pp(sorted)