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

import mysql.connector, json, os, sys, traceback

# Get the absolute path of the 'utils' directory relative to this file's location
parent_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))

# Add the parent directory to the Python path
sys.path.append(parent_path)

class SprintDBManger:
    def __init__(self, config):
        """
        Initializes a SprintDBManager instance
        Pulls MySQL credentials from local config file
        """
        # Load mysql information from config file
        self.mysql_config = config

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

    def insert_data(self, table, insert_data):
        """
        Inserts sprint summary data into the database.

        Args:
            table (str): The table that the data goes into
            insert_data (dict): The data to be inserted into specific table.

        Returns:
            int: The ID of the inserted record.
        """
        cnx = self.get_cnx()
        cursor = cnx.cursor()

        try:
            # Prepare the SQL query dynamically using dictionary keys and values
            columns = ", ".join(insert_data.keys())
            placeholders = ", ".join(["%s"] * len(insert_data))
            values = tuple(insert_data.values())

            # Insert query
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

            # Execute the query
            cursor.execute(sql, values)
            cnx.commit()
        except:
            traceback.print_exc()
            raise Exception(
                'Error occurred while inserting into boards table')

        inserted_id = cursor.lastrowid

        cnx.close()

        return inserted_id

    def get_board_data_from_db(self, board_id = None, assigned_board_id = None):
        """
        Fetches board data from the database based on user input.

        Args:
            board_id (str): The ID of the board.

        Returns:
            dict: The board data.
        """
        cnx = self.get_cnx()
        cursor = cnx.cursor()

        if board_id is not None:
            select_statement = f"SELECT json_data FROM boards WHERE board_id = '{board_id}';"
        else:
            select_statement = f"SELECT json_data FROM boards WHERE id = '{assigned_board_id}';"

        cursor.execute(select_statement)
        
        results = cursor.fetchall()
    
        return json.loads(results[0][0])

    def get_sprint_summary_from_db(self, board_id):
        """
        Fetches sprint summary data from the database for a given board ID.

        Args:
            board_id (str): The ID of the board.

        Returns:
            dict: The sprint summaries data based off board_id - will be sorted chronologically in ascending order.
        """
        cnx = self.get_cnx()
        cursor = cnx.cursor()

        select_statement = f"SELECT * FROM sprint_summary WHERE board_id = '{board_id}'; ORDER BY created_at ASC"
    
        cursor.execute(select_statement)
        
        results = cursor.fetchall()
    
        return results

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
