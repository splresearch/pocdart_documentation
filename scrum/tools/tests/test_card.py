"""
test_card.py

This module contains unit tests for the TrelloCard class, ensuring that the Card interactions
with Trello are correctly implemented.

Tests:
    - test_fetch_story_points: Tests the fetch_story_points method.
"""
import pytest, os, sys
# Import the function from helper.py
# Get the absolute path of the 'utils' directory relative to this file's location
parent_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))

# Add the parent directory to the Python path
sys.path.append(parent_path)
from trello.card import Card


def test_fetch_story_points():
    # Arrange: Define card data with story points
    test_story_points = {
        'total': 4,
        'spent': 2,
        'remaining': 2
        }
    test_card = Card(
        card_id='Noble141', 
        story_points=test_story_points,)
    # Act: Extract story points from defined Card
    story_points = test_card.get_story_points()
    total_story_points = test_card.get_total_story_points()
    spent_story_points = test_card.get_spent_story_points()
    remaining_story_points = test_card.get_remaining_story_points()
    # Assert: Verify that story points are correctly extracted for both cases
    assert test_story_points == story_points
    assert test_story_points['total'] == total_story_points
    assert test_story_points['spent'] == spent_story_points
    assert test_story_points['remaining'] == remaining_story_points

def test_set_story_points():
    # Arrange: Define card data with story points
    test_story_points = {
        'total': 4,
        'spent': 2,
        'remaining': 2
        }
    test_card = Card(
        card_id='Noble141', 
        story_points=test_story_points,)
    # Act: Change story points
    test_story_points = {
        'total': 7,
        'spent': 4,
        'remaining': 3
    }
    test_card.set_story_points(test_story_points)
    # Assert: Verify story points have changed in card
    assert test_story_points == test_card.get_story_points()
    # Act: Change story points individually
    test_card.set_total_story_points(10)
    test_card.set_spent_story_points(5)
    test_card.set_remaining_story_points(5)
    # Assert: Verify story points have changed in card
    assert test_card.get_total_story_points() == 10
    assert test_card.get_spent_story_points() == 5
    assert test_card.get_remaining_story_points() == 5
