"""Unit tests for delay helper functions used in train scripts."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sncf-train-schedule', 'skills', 'plan-journey', 'scripts'))

from get_departures import compute_delay_minutes, format_disruption


def test_compute_delay_on_time():
    assert compute_delay_minutes("20260210T140000", "20260210T140000") == 0


def test_compute_delay_late():
    assert compute_delay_minutes("20260210T140000", "20260210T140700") == 7


def test_compute_delay_early():
    assert compute_delay_minutes("20260210T140000", "20260210T135500") == -5


def test_compute_delay_invalid_returns_zero():
    assert compute_delay_minutes(None, "20260210T140000") == 0
    assert compute_delay_minutes("bad", "20260210T140000") == 0


def test_format_disruption_on_time():
    sdt = {
        "departure_date_time": "20260210T140000",
        "base_departure_date_time": "20260210T140000",
    }
    assert format_disruption(sdt, "departure_date_time") == ""


def test_format_disruption_delayed():
    sdt = {
        "departure_date_time": "20260210T140700",
        "base_departure_date_time": "20260210T140000",
    }
    assert format_disruption(sdt, "departure_date_time") == "+7min"


def test_format_disruption_early():
    sdt = {
        "departure_date_time": "20260210T135500",
        "base_departure_date_time": "20260210T140000",
    }
    assert format_disruption(sdt, "departure_date_time") == "-5min"


def test_format_disruption_no_base_time():
    sdt = {"departure_date_time": "20260210T140000"}
    assert format_disruption(sdt, "departure_date_time") == ""


def test_format_disruption_cancelled():
    sdt = {
        "departure_date_time": "20260210T140000",
        "base_departure_date_time": "20260210T140000",
        "additional_informations": ["no_departing"],
    }
    assert format_disruption(sdt, "departure_date_time") == "❌ SUPPRIMÉ"


def test_format_disruption_arrival_key():
    sdt = {
        "arrival_date_time": "20260210T160700",
        "base_arrival_date_time": "20260210T160000",
    }
    assert format_disruption(sdt, "arrival_date_time") == "+7min"


from get_arrivals import compute_delay_minutes as arr_compute_delay, format_disruption as arr_format_disruption


def test_arrivals_delay_helper_matches_departures():
    """Same logic — verify both scripts export compatible helpers."""
    assert arr_compute_delay("20260210T160000", "20260210T160500") == 5


def test_arrivals_format_disruption():
    sdt = {
        "arrival_date_time": "20260210T160500",
        "base_arrival_date_time": "20260210T160000",
    }
    assert arr_format_disruption(sdt, "arrival_date_time") == "+5min"


from plan_journey import format_journey_status


def test_journey_status_on_time():
    assert format_journey_status({}) == ""
    assert format_journey_status({"status": ""}) == ""


def test_journey_status_delayed():
    assert format_journey_status({"status": "SIGNIFICANT_DELAYS"}) == "⚠️"
    assert format_journey_status({"status": "MODIFIED_SERVICE"}) == "⚠️"


def test_journey_status_cancelled():
    assert format_journey_status({"status": "NO_SERVICE"}) == "❌ SUPPRIMÉ"
