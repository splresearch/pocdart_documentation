"""
test-get_custom_field_ids.py

This module contains unit tests for the ad-hoc script to validate the output
"""

import sys
import re
from pathlib import Path

# Add the parent directory to the Python path
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))

from bin.get_custom_field_ids import main

def test_main(capfd):
    # Call target method
    main()
    # Check for printout of associated trello card short link
    captured = capfd.readouterr()
    assert re.search("idCustomField", captured.out)
