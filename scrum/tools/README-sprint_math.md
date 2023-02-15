What is need beforehand
	json config
		where
		what
	sprint math module
		where
		what
How to run
	user-provided parameters and what they mean
Basic rundown
Example output is like

# What is the `sprint_math.py` script?
The `sprint_math.py` script is designed to make it easier for those of us at Pocdart to make Sprint calculation steps easier and take less time. It will take information about the past Sprint, using that data along with some small other points of historical data from previous other Sprints to calculate what we as a group should aim for in the Sprint we are planning for. This should make the calculation process faster and more objective.
# What is needed beforehand to run the script?
## JSON Config
There is a `config.json` file located within `/home/pocdart/config/sprint_math`. This file must be put into the same directory as the `sprint_math.py` script for it get the information it requires.
Inside of the config file, there are a few things:
    1. The "SPRINT-NOW" board ID for pulling cards and other information from the dashboard
    2. The API key used to authenticate and access the board
    3. The API token used to authenticate and access the board (yes, the key and the token are different, and both can be found in this [page](https://trello.com/power-ups/admin) under the "Sprint Math" module)
    4. The ID of the Sprint Calculation History card
    5. The ID of the UNPLANNED template card
