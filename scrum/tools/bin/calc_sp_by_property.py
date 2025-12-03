""" Print stats about story point allocation on the current sprint board
    By: label, member
"""

# Set working directry for module imports
import os
import sys
from colorama import Fore, Style
os.chdir("/home/pocdart/pocdart_documentation/scrum/tools/")
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# Import local modules
from sprint_utils import load_config
from trello.api import TrelloAPI
from trello.board import Board
def main():
    """ Generate report on Trello board stats including work type and SP totals by owner """
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
    #   Ideal workload releases more new features than internal improvements (<40% is best)
    #   These thresholds and colors are set to encourage majority User Story / Change work
    if iw_percentage > 50:
        iw_color = Fore.RED
    elif iw_percentage > 40:
        iw_color = Fore.YELLOW
    else:
        iw_color = Fore.GREEN
    # Print report to console
    print("Internal work percentage: " + iw_color + str(iw_percentage) + "%")
    print(Style.RESET_ALL)

    # SP totals stratified by owner
    # Initialize result object
    sp_by_owner = {}
    # Create owner id-name mapping
    members = trello_api.get_board_member_ids()
    owner_lookup = {value: trello_api.get_member_details(value)["fullName"] for value in members}
    # Iterate cards
    for card in board.get_cards():
        # Extract members
        id_members = card.get_id_members()
        # If members exist
        if len(id_members) > 0:
            # Use mapping to get name of first idMember listed
            name = owner_lookup[id_members[0]]
            # If first card for this name, add
            if name not in sp_by_owner.keys():
                sp_by_owner[name] = card.get_total_story_points()
            # Else increment
            else:
                sp_by_owner[name] += card.get_total_story_points()
    # Reverse sort
    sp_sorted = dict(sorted(sp_by_owner.items(), key=lambda item: item[1], reverse = True))
    # Print result to console
    print("Story points by owner:")
    for key, value in sp_sorted.items():
        print(f'{key:20}{value}')
    # Get list of owners with zero points or not listed
    no_points = [
            k for k,v in sp_by_owner.items() if v == 0
        ] + [
            y for x,y in owner_lookup.items() if y not in sp_by_owner.keys()
        ]
    no_points.sort()
    # Print result to console
    print('Members with zero story points assigned: ' + ', '.join(no_points))

if __name__ == "__main__":
    main()
