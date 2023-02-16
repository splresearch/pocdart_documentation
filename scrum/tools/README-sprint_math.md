# What is the `sprint_math.py` script?
`Sprint_math.py` is a script designed to simplify the process of calculating Sprint targets at Pocdart. It uses data from previous Sprints, along with some additional historical information, to determine what the group should aim for in the upcoming Sprint. By automating this calculation, we can save time and ensure that our targets are objective and consistent with past performance.
# What is needed beforehand to run the script?
## JSON Config
There is a `config.json` file located within `/home/pocdart/config/sprint_math`. This file must be put into the same directory as the `sprint_math.py` script for it get the information it requires.
Inside of the config file, there are a few things:
    1. The "SPRINT-NOW" board ID for pulling cards and other information from the dashboard
    2. The API key used to authenticate and access the board
    3. The API token used to authenticate and access the board (yes, the key and the token are different, and both can be found in this [page](https://trello.com/power-ups/admin) under the "Sprint Math" module)
    4. The ID of the Sprint Calculation History card
    5. The ID of the UNPLANNED template card
## Sprint Math Module
Inside of the [power-up admin panel](https://trello.com/power-ups/admin), there is a link to the "Sprint Math Module" with a key icon. Clicking that button will open up settings. The "API Key" setting contains both the API key (which can be copied) and the ability to generate a new token (done by clicking the `Token` highlighted link next to where the key is shown).
# Running the Script
Once the `config.json` has been placed in the same directory as the script, one may run the the script by doing this command into an appropriate console `Python sprint_math.py`.
Once started, the script will pull and extract most of the numbers it needs to complete its calculations. The only bits of information that are still needed must be user provided, and they are as follows:
	1. `sp_planned_total` - The number of planned Story Points (SP) for past Sprint
	2. `sprint_days_last` - The number of days in the past Sprint (default to 10)
	3. `sprint_days_next` - The number of days in the upcoming Sprint (default to 10)
	4. `total_days_missed_last` - The total days missed in the last Sprint (default to 0)
	5. `total_days_to_be_missed` - The total days missed in the upcoming Sprint (default to 0)
	6. `n_members` - The number of members to be present in the upcoming Sprint (default to 9)
All except the `sp_planned_total` can be skipped over with a single press of the `Enter` button if one wants to use the default values for each.
After those values are inputted, the script will output all the information collected from the dashboard and user, the calculations, and number of the next Sprint's SP planned total.
