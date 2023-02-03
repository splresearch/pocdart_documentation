import json
import requests
import pandas as pd
import re

# API key and token and board id should be stored in config, away from posting on GitHub
with open("config.json") as config_file:
    config_var = json.load(config_file)

def request_call(url, have_headers):
    if have_headers:
        headers = {
            "Accept": "application/json"
        }
    else:
        headers = {}

    query = {
        'key': config_var["api_key"],
        'token': config_var["api_token"]
    }

    response = requests.request(
        "GET",
        url,
        params=query,
        headers=headers
    )

    return json.loads(response)

class Card:
    def __init__(self, card_id, card_name, labels, list_id):
        self.id = card_id
        self.name = card_name
        self.labels = labels

        self.fetch_card_size()
        self.fetch_list_name(list_id)
    def fetch_card_size(self):
        # Request pluginData using id
        url = "https://api.trello.com/1/cards/" + self.id + "/pluginData"
        response_data = request_call(url=url, have_headers=False)

        # Parse request for card size
        values = re.findall(r'"size":(\d+),\s*"spent":(\d+)', response_data)
        self.size = {
            "size": int(values[0][0]),
            "spent": int(values[0][1]),
            "remaining": int(values[0][0]) - int(values[0][1])
        }
    def fetch_list(self, list_id):
        # Request list data using board id
        
        url = "https://api.trello.com/1/boards/" + config_var["board_id"] + "/lists"
        response_data = request_call(url=url, have_headers=True)

        # Parse request for matching list
        self.list_name = next(list_obj for list_obj in response_data if list_obj["id"] == list_id)["name"]

total_done_list = 0
sp_unplanned_total = 0
sp_planned_partial_completed = 0

# Request to get every card off of the sprint board
url = "https://api.trello.com/1/boards/" + config_var["board_id"] + "/cards"
response_data = request_call(url=url, have_headers=False)

# Parse request in for loop
for card in response_data:
    labels_list = card["labels"]
    card_labels = [subitem["name"] for subitem in labels_list]
    # Check to ignore monitoring cards and counting and template card in count
    # IDS NEED TO BE MOVED TO CONFIG
    if "Monitoring" in card_labels or card["id"] == config_var["sprint_calc_card"] or config_var["unplanned_template_card"] == "":
        continue

    new_card = Card(card_id=card["id"], card_name=card["name"], labels=card_labels, list_id=card["idList"])

    # Handle if unplanned
    if "UNPLANNED" in card.labels:
        sp_unplanned_total += card.size["size"]

    # Handle if in done list
    if "Done" in card.list_name:
        total_done_list += card.size["size"]
    
    # Handle if still on other parts of the board
    if "Done" not in card.labels:
        # If partially completed
        if card.size["remaining"] > 0:
            sp_planned_partial_completed += card.size["remaining"]

while True:
    user_planned_total = input("How much was planned in the previous Sprint? ") # from summary card
    try: 
        user_planned_total = int(user_planned_total)
        break
    except ValueError:
        print("Please give a valid number.")