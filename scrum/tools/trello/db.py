"""
db.py

This module contains functions for interacting with the MySQL database to store and retrieve
Trello board and story points data.

Functions:
    - insert_board_data: Inserts board data into the database.
    - insert_sprint_summary: Inserts sprint summary data into the database.
    - get_board_data_from_db: Retrieves board data from the database.
    - get_sprint_summary_from_db: Retrieves sprint summary data from the database.
"""

import mysql.connector, json, os, sys

# Get the absolute path of the 'utils' directory relative to this file's location
parent_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))

# Add the parent directory to the Python path
sys.path.append(parent_path)

# Import the function from helper.py
from utils import load_config

class SprintDBManger:
    def __init__(self):
        """
        Initializes a SprintDBManager instance
        Pulls MySQL credentials from local config file
        """
        # Load mysql information from config file
        self.mysql_config = load_config()['mysql']

    def get_cnx(self, database="default"):
        """
        Define connection agent cnx

        Args:
            database: target database name, defaults to global environment value

        Returns:
            obj: mysql connector connect object
        """
        
        if database == "default":
            target_database = self.mysql_config["database"]
        else:
            target_database = database
        cnx = mysql.connector.connect(user=self.mysql_config["user"],
                                      password=self.mysql_config["password"],
                                      host=self.mysql_config["host"],
                                      database=target_database)
        return(cnx)

    def insert_board_data(self, board_id, board_name, json_data):
        """
        Inserts board data into the database.

        Args:
            board_id (str): The Trello board ID.
            board_name (str): The Trello board name.
            json_data (dict): The JSON data of the board.

        Returns:
            int: The ID of the inserted board record.
        """
        pass

    def insert_sprint_summary(self, board_db_id, sprint_summary):
        """
        Inserts sprint summary data into the database.

        Args:
            board_db_id (int): The ID of the board record in the database.
            sprint_summary (dict): The sprint summary data.
        """
        pass

    def get_board_data_from_db(self, entry_id):
        """
        Fetches board data from the database based on user input.

        Args:
            entry_id (str): The ID of the database entry.

        Returns:
            dict: The board data.
        """
        pass

    def get_sprint_summary_from_db(self, board_id):
        """
        Fetches sprint summary data from the database for a given board ID.

        Args:
            board_id (str): The ID of the board.

        Returns:
            dict: The sprint summary data formatted as expected story points.
        """
        pass

    def execute_query(self, query, database="default", dic=False):
        """Execute generic MySQL command

        Args:
            query (str): MySQL query
            condition (str): MySQL select condition
            database (str): Which MySQL database

        Returns:
            list / list of dictionaries: MySQL query output
        """
        cnx = self.get_cnx(database)
        cursor = cnx.cursor(dictionary=dic)

        cursor.execute(query)

        result = cursor.fetchall()

        cnx.commit()
        cnx.close()

        return(result)
