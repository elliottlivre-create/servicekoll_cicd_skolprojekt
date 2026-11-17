from datetime import date

import pytest

from app.service import add_months, service_status

TODAY = date(2026, 11, 14)


def test_ok_when_service_is_far_away():
    # Arrange
    last_service = date(2026, 6, 1)

    # Act
    result = service_status("pulver", last_service, today=TODAY)

    # Assert
    assert result["next_service"] == "2027-06-01"
    assert result["status"] == "ok"


def test_snart_within_30_days():
    result = service_status("pulver", date(2025, 12, 1), today=TODAY)
    assert result["days_left"] == 17
    assert result["status"] == "snart"


def test_forsenad_when_date_has_passed():
    result = service_status("pulver", date(2025, 10, 1), today=TODAY)
    assert result["days_left"] < 0
    assert result["status"] == "forsenad"


def test_service_day_is_today_counts_as_snart():
    result = service_status("pulver", date(2025, 11, 14), today=TODAY)
    assert result["days_left"] == 0
    assert result["status"] == "snart"


def test_kolsyra_has_longer_interval():
    result = service_status("kolsyra", date(2025, 1, 10), today=TODAY)
    assert result["next_service"] == "2027-01-10"


def test_type_is_case_insensitive():
    result = service_status("  PULVER ", date(2026, 6, 1), today=TODAY)
    assert result["type"] == "pulver"


def test_unknown_type_raises_error():
    with pytest.raises(ValueError):
        service_status("glass", date(2026, 6, 1), today=TODAY)


def test_last_service_in_future_raises_error():
    with pytest.raises(ValueError):
        service_status("pulver", date(2027, 1, 1), today=TODAY)


def test_add_months_handles_leap_year():
    assert add_months(date(2024, 2, 29), 12) == date(2025, 2, 28)


def test_add_months_handles_end_of_month():
    assert add_months(date(2026, 1, 31), 1) == date(2026, 2, 28)