"""
utils.py

This module contains utility functions for loading configuration data.
"""

import json

def load_config(file_path):
    """
    Loads the configuration from a JSON file.

    Args:
        file_path (str): The path to the configuration file.

    Returns:
        dict: The configuration data.
    """
    with open(file_path, "r", encoding="utf-8") as config_file:
        return json.load(config_file)

def load_test_board_data(file_path, return_str = False):
    with open(file_path, "r", encoding="utf-8") as test_board_data_file:
        if (return_str == False):
            return json.load(test_board_data_file)
        else:
            return json.dumps(json.load(test_board_data_file))