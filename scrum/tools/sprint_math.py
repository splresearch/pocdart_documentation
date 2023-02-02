import json
import requests
import pandas as pd
import re
import requests

# API key and token and board id should be stored in config, away from posting on GitHub

list_cards = []

def request_call(url, have_headers):
    if have_headers:
        headers = {
            "Accept": "application/json"
        }
    else:
        headers = {}

    query = {
        'key': 'APIKey',
        'token': 'APIToken'
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
        self.card_id = card_id
        self.card_name = card_name
        self.labels = labels

        self.fetch_card_size()
        self.fetch_list_name(list_id)
    def fetch_card_size(self):
        # Request pluginData using id
        url = "https://api.trello.com/1/cards/" + self.card_id + "/pluginData"
        response_data = request_call(url=url, have_headers=False)

        # Parse request for card size
        values = re.findall(r'"size":(\d+),\s*"spent":(\d+)', response_data)
        self.card_size = {
            "size": int(values[0][0]),
            "spent": int(values[0][1]),
            "remaining": int(values[0][0]) - int(values[0][1])
        }
    def fetch_list(self, list_id):
        # Request list data using board id
        
        url = "https://api.trello.com/1/boards/" + board_id + "/lists"
        response_data = request_call(url=url, have_headers=True)

        # Parse request for matching list
        self.list_name = next(item for item in response_data if item["id"] == list_id)["name"]

# Request to get every card off of the sprint board
url = "https://api.trello.com/1/boards/" + board_id + "/cards"
response_data = request_call(url=url, have_headers=False)

# Parse request in for loop
for item in response_data:
    card_id = item["id"]
    card_name = item["name"]
    list_id = item["idList"]

    list_labels = item["labels"]
    card_labels = [subitem["name"] for subitem in item]

    new_card = Card(card_id=card_id, card_name=card_name, labels=card_labels, list_id=list_id)
    list_cards.append(new_card)

while True:
    user_planned_total = input("How much was planned in the previous Sprint? ") # from summary card
    try: 
        user_planned_total = int(user_planned_total)
        break
    except ValueError:
        print("Please give a valid number.")