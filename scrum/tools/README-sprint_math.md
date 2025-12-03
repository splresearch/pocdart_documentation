# What is the `sprint_math.py` script?
`Sprint_math.py` is a script designed to simplify the process of calculating Sprint targets. It uses data from previous Sprints, along with some additional historical information, to recommend a story point target for the upcoming Sprint.
# What is needed beforehand to run the script?
## JSON Config
There is a `config.json` file located in `/home/pocdart/config/sprint_math`. This file must be copied into the same directory as `sprint_math.py`.
Inside of the config file, there are a few things:
1. The "SPRINT-NOW" board ID for pulling cards and other information from the dashboard
2. The Trello API key used to authenticate and access the board
3. The Trello API token used to authenticate and access the board (the key and the token are different, and both can be found in this [page](https://trello.com/power-ups/admin) under the "Sprint Math" module)
4. The ID of the Sprint Calculation History card
5. The ID of the UNPLANNED template card
6. The IDs of the custom fields that contain Story Point allocations
7. MySQL connection parameters, for storing the calculation results

## Sprint Math Module
Inside of the [power-up admin panel](https://trello.com/power-ups/admin), there is a link to the "Sprint Math Module" with a key icon. Clicking that button will open up settings. The "API Key" setting contains both the API key (which can be copied) and the ability to generate a new token (done by clicking the `Token` highlighted link next to where the key is shown).

# Running the Script
Once the `config.json` has been placed in the same directory as the script, run it with `python sprint_math.py`.
The script will pull and extract most of the numbers it needs to complete its calculations. The only bits of information that are still needed must be user provided, and they are as follows:
1. `sp_planned_total` - The number of planned Story Points (SP) for past Sprint
2. `sprint_days_last` - The number of days in the past Sprint (default to 15)
3. `sprint_days_next` - The number of days in the upcoming Sprint (default to 15)
4. `total_days_missed_last` - The total days missed in the last Sprint (default to 0)
5. `total_days_to_be_missed` - The total days missed in the upcoming Sprint (default to 0)
6. `n_members` - The number of members to be present in the upcoming Sprint (default to 8)
All except the `sp_planned_total` can be skipped over with a single press of the `Enter` button if one wants to use the default values for each.
After those values are inputted, the script will output all the information collected from the dashboard and user, the calculations, and number of the next Sprint's SP planned total.

# Ad-hoc scripts
Helper scripts are stored in the scrum/tools/bin/ directory.
1. `calc_sp_by_property.py` - Print Story Points distribution by label and owner
2. `convert_id_to_short_link.py` - Get a Trello card's short link from the ID, useful for troubleshooting
3. `get_card_ids.py` - Print a pipe-delimited list of all Trello card short links, useful for grepping github branch reports
4. `get_custom_field_ids.py` - Print the custom fields object for config population
