"""
test-get_card_ids.py

This module contains unit tests for the ad-hoc script to validate the output
"""

import sys
import re
from pathlib import Path

# Add the parent directory to the Python path
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))

from bin.get_card_ids import main

def test_main(capfd):
    # Call target method
    main()
    # Check for presence of trello card short link in pipe-delimited output
    captured = capfd.readouterr()
    expected_message = r"Q9EAW7j2\|"
    assert re.search(expected_message, captured.out)
