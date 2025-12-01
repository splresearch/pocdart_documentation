"""
test_card.py

This module contains unit tests for the Card class, ensuring that the Card interactions
are correctly implemented.

Tests:
    - test_get_story_points: Tests the retrieval of story points.
    - test_set_story_points: Tests the modification of story points.
"""

import sys
from pathlib import Path

import pytest

# Add the parent directory to the Python path
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))

from trello.card import Card  # Import the Card class to be tested


def test_get_story_points():
    """
    Tests the retrieval of story points from a Card instance.
    """
    # Arrange: Define card data with story points
    test_story_points = {
        'total': 4,
        'spent': 2,
        'remaining': 2
    }
    test_card = Card(
        card_id='Noble141',
        story_points=test_story_points
    )

    # Act: Retrieve story points using getter methods
    story_points = test_card.get_story_points()
    total_story_points = test_card.get_total_story_points()
    spent_story_points = test_card.get_spent_story_points()
    remaining_story_points = test_card.get_remaining_story_points()

    # Assert: Verify that story points are correctly retrieved
    assert story_points == test_story_points
    assert total_story_points == test_story_points['total']
    assert spent_story_points == test_story_points['spent']
    assert remaining_story_points == test_story_points['remaining']


def test_set_story_points():
    """
    Tests the modification of story points in a Card instance.
    """
    # Arrange: Define initial card data with story points
    initial_story_points = {
        'total': 4,
        'spent': 2,
        'remaining': 2
    }
    test_card = Card(
        card_id='Noble141',
        story_points=initial_story_points
    )

    # Act: Change story points using set_story_points method
    new_story_points = {
        'total': 7,
        'spent': 4,
        'remaining': 3
    }
    test_card.set_story_points(new_story_points)

    # Assert: Verify that story points have been updated
    assert test_card.get_story_points() == new_story_points

    # Act: Change story points individually using setter methods
    test_card.set_total_story_points(10)
    test_card.set_spent_story_points(5)
    test_card.set_remaining_story_points(5)

    # Assert: Verify that individual story points have been updated
    assert test_card.get_total_story_points() == 10
    assert test_card.get_spent_story_points() == 5
    assert test_card.get_remaining_story_points() == 5
