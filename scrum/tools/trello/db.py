"""
db.py

This module contains the `SprintDBManager` class for interacting 
    with the MySQL database to store and retrieve
    Trello board and story points data.

Classes:
    - SprintDBManager: Manages database operations for sprint data.

Example Usage:
    db_manager = SprintDBManager(config)
    db_manager.insert_data(table='boards', insert_data=board_data)
    board_data = db_manager.get_board_data_from_db(board_id='your_board_id')
"""

import json
import traceback
import mysql.connector


class SprintDBManager:
    def __init__(self, config):
        """
        Initializes a SprintDBManager instance with MySQL configuration.

        Args:
            config (dict): MySQL configuration parameters.
        """
        self.mysql_config = config

    def get_cnx(self, database="default"):
        """
        Establishes a connection to the MySQL database.

        Args:
            database (str, optional): Target database name. 
                Defaults to the one specified in the config.

        Returns:
            mysql.connector.connection.MySQLConnection: A MySQL connection object.
        """
        if database == "default":
            target_database = self.mysql_config["database"]
        else:
            target_database = database

        cnx = mysql.connector.connect(
            user=self.mysql_config["user"],
            password=self.mysql_config["password"],
            host=self.mysql_config["host"],
            database=target_database
        )
        return cnx

    def insert_data(self, table, insert_data):
        """
        Inserts data into a specified table in the database.

        Args:
            table (str): The name of the table to insert data into.
            insert_data (dict): A dictionary of data to insert (column names as keys).

        Returns:
            int: The ID of the inserted record.

        Raises:
            Exception: If an error occurs during the insertion.
        """
        cnx = self.get_cnx()
        cursor = cnx.cursor()

        try:
            # Prepare the SQL query dynamically using dictionary keys and
            # values
            columns = ", ".join(insert_data.keys())
            placeholders = ", ".join(["%s"] * len(insert_data))
            values = tuple(insert_data.values())

            # Insert query
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

            # Execute the query
            cursor.execute(sql, values)
            cnx.commit()

            inserted_id = cursor.lastrowid
        except Exception as e:
            traceback.print_exc()
            raise Exception(
                'Error occurred while inserting into the table') from e
        finally:
            cnx.close()

        return inserted_id

    def get_board_data_from_db(self, board_id=None, assigned_board_id=None):
        """
        Retrieves board data from the database.

        Args:
            board_id (str, optional): The Trello board ID.
            assigned_board_id (str, optional): The internal database ID of the board.

        Returns:
            dict: The board data in JSON format.

        Raises:
            Exception: If the board data is not found.
        """
        cnx = self.get_cnx()
        cursor = cnx.cursor()

        try:
            if board_id is not None:
                select_statement = "SELECT json_data FROM boards WHERE board_id = %s;"
                cursor.execute(select_statement, (board_id,))
            elif assigned_board_id is not None:
                select_statement = "SELECT json_data FROM boards WHERE id = %s;"
                cursor.execute(select_statement, (assigned_board_id,))
            else:
                raise ValueError(
                    "Either 'board_id' or 'assigned_board_id' must be provided.")

            results = cursor.fetchall()

            if not results:
                raise Exception("Board data not found in the database.")

            board_data_json = results[0][0]
            return json.loads(board_data_json)
        finally:
            cnx.close()

    def get_sprint_summary_from_db(self, board_id):
        """
        Retrieves sprint summary data from the database for a given board ID.

        Args:
            board_id (str): The Trello board ID.

        Returns:
            list: A list of sprint summary records sorted chronologically in ascending order.

        Raises:
            Exception: If an error occurs during the retrieval.
        """
        cnx = self.get_cnx()
        cursor = cnx.cursor(dictionary=True)

        try:
            select_statement = """
                SELECT * FROM sprint_summary WHERE board_id = %s ORDER BY created_at ASC;
            """
            cursor.execute(select_statement, (board_id,))

            results = cursor.fetchall()
            return results
        finally:
            cnx.close()

    def execute_query(self, query, database="default", dic=False):
        """
        Executes a generic MySQL query.

        Args:
            query (str): The MySQL query to execute.
            database (str, optional): The database to use. Defaults to 'default'.
            dic (bool, optional): Whether to return results as dictionaries. Defaults to False.

        Returns:
            list: The query results.

        Raises:
            Exception: If an error occurs during query execution.
        """
        cnx = self.get_cnx(database)
        cursor = cnx.cursor(dictionary=dic)

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            cnx.commit()
            return result
        finally:
            cnx.close()
