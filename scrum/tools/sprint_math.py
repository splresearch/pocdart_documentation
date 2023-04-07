# IMPORTS
# ======
import json
import statistics
import math
import re
import requests

# API key and token and board id should be stored in config, away from
# posting on GitHub
with open("config.json", "r", encoding="utf-8") as config_file:
    config_var = json.load(config_file)



# HELPER FUNCTIONS
# ======
def request_call(url, have_headers):
    """Makes a GET request to the specified board using the requests library.

    Args:
        url: str, the URL to make the GET request to.
        have_headers: bool, specifies if the request should include headers.

    Returns:
        dict, the JSON response from the API.
    """
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
        headers=headers,
        timeout=60
    )

    return response.json()



# CARD CLASS
# ======
class Card:
    """Representation of a Trello card.

    Attributes:
        id: str, the ID of the card.
        name: str, the name of the card.
        labels: list, the labels associated with the card.
        size: dict, the size of the card and the amount of time spent/remaining on it.
        list_name: str, the name of the list the card is associated with.

    Methods:
        fetch_card_size: Retrieves the size of the card.
        fetch_list_name: Retrieves the name of the list the card is associated with.
    """
    def __init__(self, card_id, card_name, labels, list_id):
        self._id = card_id
        self.name = card_name
        self.labels = labels

        self.fetch_card_size()
        self.fetch_list_name(list_id)

    def fetch_card_size(self):
        """Retrieves the size of the card."""
        url = "https://api.trello.com/1/cards/" + self._id + "/pluginData"
        plugin_data = request_call(url=url, have_headers=False)

        # If the card size module has not been filled out, set everything to zero
        if not plugin_data:
            print(
                f"This card, {self.name}, has not been estimated, assigned values of 0")
            self.size = {
                "size": 0,
                "spent": 0,
                "remaining": 0
            }
        else:
            # Parse request for card size
            values = re.findall(
                r'"size":(\d+),\s*"spent":(\d+)',
                plugin_data[0]['value'])
            self.size = {
                "size": int(values[0][0]),
                "spent": int(values[0][1]),
                "remaining": int(values[0][0]) - int(values[0][1])
            }

    def fetch_list_name(self, list_id):
        """Retrieves the name of the list the card is associated with.

        Args:
            list_id: str, Python list of the Trello list IDs to retrieve the name for.
        """
        self.list_name = next(
            list_obj for list_obj in sprint_lists if list_obj["id"] in list_id)["name"]



# INPUTS
# ======
# From card size module
TOTAL_DONE_LIST = 0  # card size > list > done + post-mortem
SP_UNPLANNED_TOTAL = 0  # card size > label > unplanned

# count, spent on planned cards that are not in the done list
SP_PLANNED_PARTIAL_COMPLETED = 0

SP_UNPLANNED_REMAINING = 0  # count, remaining
# count, spent on unplanned cards that are not in the done list
SP_UNPLANNED_PARTIAL_COMPLETED = 0

# count - any additional points spent above planned card size on cards in done
SP_RETRO_COMPLETED = 0
SP_RETRO_LEFTOVER = 0  # total retro newly created in other lists

# Pull board id from config
board_id = config_var["board_id"]
# Request to get every card off of the sprint board
cards_url = f"https://api.trello.com/1/boards/{board_id}/cards"
sprint_cards = request_call(url=cards_url, have_headers=False)
# Request list data using board id
lists_url = f"https://api.trello.com/1/boards/{board_id}/lists"
sprint_lists = request_call(url=lists_url, have_headers=True)

# Parse every card in request
for card in sprint_cards:
    # Gather all labels for current card
    labels_list = card["labels"]
    card_labels = [subitem["name"] for subitem in labels_list]
    # Check to ignore template card in count
    if card["id"] == config_var["unplanned_template_card"]:
        continue
    # If the card is the Sprint calc history card,
    #   pull out all the unplanned story points from previous Sprints
    if card["id"] == config_var["sprint_calc_card"]:
        unplanned_past_sprints = re.findall(
            r"unplanned: \*{2}(\d+)", card["desc"], re.IGNORECASE)
        unplanned_past_sprints = [int(i) for i in unplanned_past_sprints]
        continue

    new_card = Card(card_id=card["id"], card_name=card["name"],
                    labels=card_labels, list_id=card["idList"])

    # Handle if in monitoring
    if "Monitoring" in new_card.list_name:
        continue

    # Handle if unplanned
    if "UNPLANNED" in new_card.labels:
        SP_UNPLANNED_TOTAL += new_card.size["size"]

    # Handle if in done list
    if "Done" in new_card.list_name:
        TOTAL_DONE_LIST += new_card.size["spent"]
        # If Retro
        if "RETRO" in new_card.labels:
            SP_RETRO_COMPLETED += new_card.size["spent"]

    # Handle if still on other parts of the board
    if "Done" not in new_card.list_name:
        # If unplanned
        if "UNPLANNED" in new_card.labels:
            if new_card.size["spent"] > 0:
                SP_UNPLANNED_PARTIAL_COMPLETED += new_card.size["spent"]
            elif new_card.size["spent"] == 0:
                SP_UNPLANNED_REMAINING += new_card.size["remaining"]
        # If Retro
        elif "RETRO" in new_card.labels:
            SP_RETRO_LEFTOVER += new_card.size["remaining"]
        # If partially completed
        elif new_card.size["spent"] > 0:
            SP_PLANNED_PARTIAL_COMPLETED += new_card.size["spent"]



# CALCULATIONS CLASS
# ============
class SprintMath:
    """A class that performs calculations related to the current sprint and the next planned sprint.

    Args:
        sp_unplanned_total (int): The total number 
            of unplanned story points.
        sp_unplanned_remaining (int): The remaining number 
            of unplanned story points.
        sp_unplanned_partial_completed (int): The number of 
            partially completed unplanned story points.
        total_done_list (int): The total number of completed 
            story points across all lists.
        sp_planned_partial_completed (int): The number of partially 
            completed planned story points.
        sp_retro_completed (int): The number of story points 
            spent above the planned size.
        sp_retro_leftover (int): The number of leftover story points 
            from the above mentioned story points.
        unplanned_past_sprints (int): The number of unplanned story 
            points from the past sprints.

    Attributes:
        sp_planned_total (int): The total number of planned story 
            points for the current sprint.
        sp_unplanned_done_list (int): The number of completed 
            unplanned story points.
        sp_planned_completed (int): The number of completed 
            planned story points.
        sp_planned_leftover (int): The number of leftover 
            planned story points.
        sp_unplanned_completed (int): The total number of 
            completed unplanned story points.
        sp_retro_total (int): The total number of 
            retro story points.
        sp_next_sprint (int): The target planned 
            points for the next sprint.

    Methods:
        __init__(gathered_sp_unplanned_total,
                gathered_sp_unplanned_remaining,
                gathered_sp_unplanned_partial_completed,
                gathered_total_done_list,
                gathered_sp_planned_partial_completed,
                gathered_sp_retro_completed,
                gathered_sp_retro_leftover,
                gathered_unplanned_past_sprints):
            Initializes the SprintMath object and calculates extra current sprint inputs.

        calc_current_sprint(self):
            Calculates extra current sprint inputs used 
                later on for other calculations or for the final output.

        get_long_sprint_controls(self):
            Prompts the user to enter values for sprint control variables.

        validate_user_input(self, user_input):
            Validates the user input to ensure it is a valid integer.

        calc_planned_next_sprint(self):
            Calculates the target planned points for the next sprint. 
                Assigns result to sp_next_sprint of current object.
    """
    def __init__(self, gathered_sp_unplanned_total = 0,
                 gathered_sp_unplanned_remaining = 0,
                 gathered_sp_unplanned_partial_completed = 0,
                 gathered_total_done_list = 0,
                 gathered_sp_planned_partial_completed = 0,
                 gathered_sp_retro_completed = 0,
                 gathered_sp_retro_leftover = 0,
                 gathered_unplanned_past_sprints = 0):
        # Assigning everything captured for calculations later on
        self.sp_unplanned_total = gathered_sp_unplanned_total
        self.sp_unplanned_remaining = gathered_sp_unplanned_remaining
        self.sp_unplanned_partial_completed = gathered_sp_unplanned_partial_completed
        self.total_done_list = gathered_total_done_list
        self.sp_planned_partial_completed = gathered_sp_planned_partial_completed
        self.sp_retro_completed = gathered_sp_retro_completed
        self.sp_retro_leftover = gathered_sp_retro_leftover
        self.unplanned_past_sprints = gathered_unplanned_past_sprints

        # Ask user for how much is planned for the upcoming Sprint
        self.sp_planned_total = input(
            "How much was planned for this Sprint? ")  # from summary card
        self.sp_planned_total = self.validate_user_input(self.sp_planned_total)

        # Calculate extra current sprint inputs
        self.calc_current_sprint()

    def calc_current_sprint(self):
        """Calculate extra current sprint inputs used later 
            on for other calculations or for the final output
        """
        # unplanned points completed = total unplanned - remaining
        # intermediary to calculate sp_planned_completed
        self.sp_unplanned_done_list = self.sp_unplanned_total - \
            self.sp_unplanned_remaining - self.sp_unplanned_partial_completed
        # planned points completed = total completed + partial done on any other lists +
        #   additional spent above planned/total in done - unplanned completed
        # (note: total_completed does not reflect "sp_retro_completed"
        #   (i.e. additional SP spent above planned size))
        self.sp_planned_completed = self.total_done_list + \
            self.sp_planned_partial_completed - self.sp_unplanned_done_list

        # Planned left over
        self.sp_planned_leftover = self.sp_planned_total - self.sp_planned_completed
        # Total unplanned completed
        self.sp_unplanned_completed = self.sp_unplanned_done_list + self.sp_unplanned_partial_completed
        # Total retro: indicates problem in discovery
        self.sp_retro_total = self.sp_retro_completed + self.sp_retro_leftover

        # Calculate the next Sprint
        self.sp_next_sprint = self.calc_planned_next_sprint()

    def get_long_sprint_controls(self):
        """Prompts the user to enter values for sprint control variables.
        Args:
            defaults: A list of default values for each sprint control variable.
        Returns:
            A list of values entered by the user, with default values used if no input
            was provided.
        """
        variables = [
            "last Sprint days",
            "next Sprint days",
            "total days missed last Sprint",
            "total days planned missed next Sprint",
            "members working this coming Sprint"]
        defaults = [10, 10, 0, 0, 9]

        sprint_controls = []
        # For every Sprint control, get user requested value
        for i, _ in enumerate(defaults):
            default = defaults[i]
            var = variables[i]
            user_input = input(
                f"Enter number of {var} (default: {str(default)}): ")
            if user_input == "":
                sprint_controls.append(default)
            else:
                sprint_controls.append(self.validate_user_input(user_input))
        # Return user's selected controls for next Sprint calculation
        return sprint_controls

    def validate_user_input(self, user_input):
        """Validates the user input to ensure it is a valid integer.

        Args:
            user_input: str, the input provided by the user.

        Returns:
            int, the validated user input as an integer.
        """
        while True:
            try:
                user_input = int(user_input)
                break
            except ValueError:
                user_input = input("Invalid input; enter a number: ")
        return user_input

    def calc_planned_next_sprint(self):
        """Calculates the target planned points for the next sprint. 
            Assigns result to sp_next_sprint of current object
        """
        # Calculate previous Sprints' unplanned points for reference
        avg_unplanned = statistics.median(self.unplanned_past_sprints)
        # Controls for things such as long sprints, vacation, etc.
        sprint_days_last, sprint_days_next, total_days_missed_last, total_days_to_be_missed, n_members = self.get_long_sprint_controls()

        length_adjustment = sprint_days_last / sprint_days_next
        pto_adjustment = (total_days_to_be_missed -
                          total_days_missed_last) / n_members

        return math.ceil((self.sp_planned_completed + self.sp_unplanned_completed -
                                avg_unplanned) / length_adjustment - pto_adjustment)

# Call the calc function to get what next Sprint's estimate number of points should be
calc_obj = SprintMath(SP_UNPLANNED_TOTAL, SP_UNPLANNED_REMAINING, SP_UNPLANNED_PARTIAL_COMPLETED,
                        TOTAL_DONE_LIST, SP_PLANNED_PARTIAL_COMPLETED, SP_RETRO_COMPLETED,
                        SP_RETRO_LEFTOVER, unplanned_past_sprints)



# OUTPUT
# ======
def output_current():
    """
    Prints out the current status of the sprint.
    """
    print(
        f"SP: Planned {str(calc_obj.sp_planned_total)}(T), {str(calc_obj.sp_planned_completed)}(A) (+{str(calc_obj.sp_retro_completed)} retro completed)\n")
    print(
        f"SP: Unplanned {str(calc_obj.sp_unplanned_total)}(T), {str(calc_obj.sp_unplanned_completed)}(A)\n")
    print(f"{str(calc_obj.sp_planned_leftover - calc_obj.sp_retro_completed)}(L.O.); {str(calc_obj.sp_retro_leftover)} Retro into next sprint\n")
    print(f"SP: Target for next sprint: {str(calc_obj.sp_next_sprint)}\n")


def output_proposal():
    """
    Outputs the proposal for SP (Story Points) for the next sprint.
    """
    # adjust sp_planned_completed
    sp_planned_completed = calc_obj.total_done_list + \
        calc_obj.sp_planned_partial_completed - calc_obj.sp_unplanned_done_list

    print(
        f"SP Planned   : {str(calc_obj.sp_planned_total)}(T), {str(sp_planned_completed)}(A) {str(calc_obj.sp_planned_leftover)}(LO)")
    print(
        f"SP Unplanned   : {str(calc_obj.sp_unplanned_total)}(T), {str(calc_obj.sp_unplanned_completed)}(A) {str(calc_obj.sp_unplanned_remaining)}(LO)")
    print(
        f"SP Retro   : {str(calc_obj.sp_retro_total)}(T), {str(calc_obj.sp_retro_completed)}(A) {str(calc_obj.sp_retro_leftover)}(LO)")
    print("======================")
    print("SP: Target for next sprint: " + str(calc_obj.sp_next_sprint))


output_current()
print("`````````````````````````````````````````````````````````\n")
output_proposal()
