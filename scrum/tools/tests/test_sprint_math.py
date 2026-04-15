"""
test_sprint_math.py

Unit tests for the compute_recommendation function in sprint_math.py
Uses plain dicts to simulate sprint_summary DB rows. No DB or API needed

Test Cases:
    - test_basic_calculation: Verifies correct output with 6 identical sprints
    - test_fewer_than_6_sprints: Works with fewer sprints than the 6-sprint lookback
    - test_leftover_subtraction: Unplanned/retro remaining are subtracted
    - test_ceiling_applied: Result is always rounded up via math.ceil
    - test_returns_breakdown_dict: Return value contains all expected keys
    - test_uses_last_6_only: Only the most recent 6 sprints influence the result
    - test_all_sprints_zero_available_days: Raises ValueError when no usable data exists
    - test_pto_exceeds_next_sprint_capacity: Raises ValueError when next sprint has no available days
    - test_leftovers_exceed_capacity_floors_at_zero: Recommendation floors at 0 when leftovers > raw capacity
"""

import math
import sys
from pathlib import Path

import pytest

parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))

from sprint_math import compute_recommendation


def make_sprint_summary(
    start_date="2026-01-01",
    length_days=10,
    members=8,
    vacation_days=0,
    planned_completed=10,
    unplanned_completed=3,
    retro_completed=2,
    unplanned_remaining=1,
    retro_remaining=1,
    **kwargs,
):
    """Generate a sprint_summary dict with controllable values"""
    return {
        "start_date": start_date,
        "length_days": length_days,
        "members": members,
        "vacation_days": vacation_days,
        "planned_completed": planned_completed,
        "unplanned_completed": unplanned_completed,
        "retro_completed": retro_completed,
        "planned_total": kwargs.get("planned_total", planned_completed),
        "planned_remaining": kwargs.get("planned_remaining", 0),
        "unplanned_total": kwargs.get("unplanned_total", unplanned_completed),
        "unplanned_remaining": unplanned_remaining,
        "retro_total": kwargs.get("retro_total", retro_completed),
        "retro_remaining": retro_remaining,
    }


@pytest.fixture
def default_sprint_controls():
    return {
        "next_sprint_days": 10,
        "members": 8,
        "missed_next_sprint": 0,
        "last_sprint_days": 10,
        "missed_last_sprint": 0,
    }


class TestComputeRecommendation:
    def test_basic_calculation(self, default_sprint_controls):
        """6 identical sprints, result should match hand calculation"""
        # Generate 6 past sprints
        sprints = [make_sprint_summary() for _ in range(6)]  # 10+3+2=15 pts, 80 days

        # Compute the recommendations
        result = compute_recommendation(sprints, default_sprint_controls)

        # Check that the results matches expected values
        # Check rate
        expected_rate = 15 / 80  # 0.1875
        # Check raw SP score before subtraction
        expected_raw = expected_rate * 80  # 15.0
        # Check recommendation after subtracting leftovers (1 unplanned + 1 retro)
        expected = math.ceil(expected_raw - 1 - 1)  # 13
        # Assert the recommendation
        assert result["recommendation"] == expected
        # Assert the rates are the same
        assert result["median_rate"] == pytest.approx(expected_rate)

    def test_fewer_than_6_sprints(self, default_sprint_controls):
        """3 sprints, should work with whatever is available"""
        # Only 3 sprints available instead of 6
        sprints = [make_sprint_summary() for _ in range(3)]

        result = compute_recommendation(sprints, default_sprint_controls)

        # Same math as basic: rate=0.1875, raw=15, minus 1, minus 1 = 13
        assert result["recommendation"] == 13
        assert len(result["sprint_rates"]) == 3
        assert result["median_rate"] == pytest.approx(15 / 80)
        assert result["next_available_member_days"] == 80
        assert result["raw_capacity"] == pytest.approx(15.0)
        assert result["median_unplanned_remaining"] == pytest.approx(1.0)
        assert result["median_retro_remaining"] == pytest.approx(1.0)

    def test_leftover_subtraction(self, default_sprint_controls):
        """Nonzero unplanned_remaining and retro_remaining are subtracted"""
        # Each sprint has 5 unplanned remaining and 3 retro remaining
        sprints = [
            make_sprint_summary(unplanned_remaining=5, retro_remaining=3)
            for _ in range(6)
        ]

        result = compute_recommendation(sprints, default_sprint_controls)

        # rate=15/80=0.1875, raw=15.0, minus 5 unplanned, minus 3 retro = 7
        expected = math.ceil(15.0 - 5 - 3)
        assert result["recommendation"] == expected
        assert result["median_unplanned_remaining"] == pytest.approx(5.0)
        assert result["median_retro_remaining"] == pytest.approx(3.0)

    def test_ceiling_applied(self, default_sprint_controls):
        """Result should be math.ceil'd when calculation is fractional"""
        # 17 pts / 80 days = 0.2125, but PTO of 3 makes next_available = 77
        #   This produces a fraction that should be rounded
        # Copy defaults but override missed_next_sprint to 3
        controls = {**default_sprint_controls, "missed_next_sprint": 3}
        sprints = [
            make_sprint_summary(
                planned_completed=12, unplanned_completed=3, retro_completed=2,
                unplanned_remaining=1, retro_remaining=1,
            )
            for _ in range(6)
        ]

        result = compute_recommendation(sprints, controls)

        # rate=17/80=0.2125, raw=0.2125*77=16.3625, minus 1, minus 1 = 14.3625 -> 15
        expected_raw = (17 / 80) * 77
        expected = math.ceil(expected_raw - 1 - 1)
        assert result["recommendation"] == expected
        assert result["recommendation"] == 15
        assert result["median_rate"] == pytest.approx(17 / 80)
        assert result["next_available_member_days"] == 77
        assert result["raw_capacity"] == pytest.approx(expected_raw)
        assert result["median_unplanned_remaining"] == pytest.approx(1.0)
        assert result["median_retro_remaining"] == pytest.approx(1.0)

    def test_returns_breakdown_dict(self, default_sprint_controls):
        """Return value is a dict with all expected keys"""
        sprints = [make_sprint_summary() for _ in range(6)]

        result = compute_recommendation(sprints, default_sprint_controls)

        expected_keys = {
            "recommendation",
            "median_rate",
            "next_available_member_days",
            "raw_capacity",
            "median_unplanned_remaining",
            "median_retro_remaining",
            "unplanned_remainders",
            "retro_remainders",
            "sprint_rates",
        }
        assert set(result.keys()) == expected_keys
        assert isinstance(result["sprint_rates"], list)
        assert len(result["sprint_rates"]) == 6

    def test_uses_last_6_only(self, default_sprint_controls):
        """When more than 6 sprints are passed, only the last 6 are used"""
        # First 4 sprints have a very different rate (0.5) than last 6 (0.1875)
        old_sprints = [
            make_sprint_summary(planned_completed=30, unplanned_completed=6, retro_completed=4,
                                unplanned_remaining=0, retro_remaining=0)
            for _ in range(4)
        ]
        recent_sprints = [
            make_sprint_summary(unplanned_remaining=0, retro_remaining=0)
            for _ in range(6)
        ]
        all_sprints = old_sprints + recent_sprints

        result = compute_recommendation(all_sprints, default_sprint_controls)

        # Should use the recent rate (0.1875), not be influenced by old (0.5)
        assert result["median_rate"] == pytest.approx(15 / 80)
        assert len(result["sprint_rates"]) == 6
        assert result["next_available_member_days"] == 80
        assert result["raw_capacity"] == pytest.approx(15.0)
        assert result["median_unplanned_remaining"] == pytest.approx(0.0)
        assert result["median_retro_remaining"] == pytest.approx(0.0)

    def test_skips_sprints_with_zero_available_days(self, default_sprint_controls):
        """Sprints where available_member_days <= 0 should be skipped"""
        # One bad sprint with vacation_days == capacity (80 - 80 = 0 available days)
        bad_sprint = make_sprint_summary(vacation_days=80)
        good_sprints = [
            make_sprint_summary(unplanned_remaining=0, retro_remaining=0)
            for _ in range(6)
        ]
        all_sprints = [bad_sprint] + good_sprints

        result = compute_recommendation(all_sprints, default_sprint_controls)

        # Bad sprint skipped, only the 6 good ones used
        assert result["median_rate"] == pytest.approx(15 / 80)
        assert len(result["sprint_rates"]) == 6
        assert result["next_available_member_days"] == 80
        assert result["raw_capacity"] == pytest.approx(15.0)
        assert result["median_unplanned_remaining"] == pytest.approx(0.0)
        assert result["median_retro_remaining"] == pytest.approx(0.0)

    def test_all_sprints_zero_available_days(self, default_sprint_controls):
        """All sprints have zero available days, should raise ValueError"""
        # Every sprint has vacation_days == capacity
        sprints = [make_sprint_summary(vacation_days=80) for _ in range(3)]

        with pytest.raises(ValueError, match="No valid sprint data found"):
            compute_recommendation(sprints, default_sprint_controls)

    def test_pto_exceeds_next_sprint_capacity(self, default_sprint_controls):
        """PTO exceeds next sprint member-days, should raise ValueError"""
        # Copy defaults but override missed_next_sprint to 100 (exceeds capacity of 10*8 = 80)
        controls = {**default_sprint_controls, "missed_next_sprint": 100}
        sprints = [make_sprint_summary() for _ in range(6)]

        with pytest.raises(ValueError, match="available member-days"):
            compute_recommendation(sprints, controls)

    def test_leftovers_exceed_capacity_floors_at_zero(self, default_sprint_controls):
        """When median leftovers exceed raw capacity, recommendation floors at 0"""
        # Very low completion rate (2/80 = 0.025, raw = 2.0) but huge leftovers (5+5 = 10)
        #   raw - leftovers = 2.0 - 10 = -8, should floor to 0
        sprints = [
            make_sprint_summary(
                planned_completed=1, unplanned_completed=1, retro_completed=0,
                unplanned_remaining=5, retro_remaining=5,
            )
            for _ in range(6)
        ]

        result = compute_recommendation(sprints, default_sprint_controls)

        assert result["recommendation"] == 0
        assert result["raw_capacity"] == pytest.approx(2.0)
        assert result["median_unplanned_remaining"] == pytest.approx(5.0)
        assert result["median_retro_remaining"] == pytest.approx(5.0)