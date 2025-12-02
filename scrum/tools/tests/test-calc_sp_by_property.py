"""
test-calc_sp_by_property.py

Unit tests for the python script. Asserts output contains expected text
"""

import sys
import re
from pathlib import Path
import pytest

# Add the parent directory to the Python path
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))

from bin.calc_sp_by_property import main

def test_main(capfd):
    # Call target method
    main()
    # Check for printout of internal work percentage
    captured = capfd.readouterr()
    expected_message = r"Internal work percentage: "
    assert re.search(expected_message, captured.out)
