from datetime import datetime
from unittest.mock import patch
import pytest

from services import booking_service_srv
from freezegun import freeze_time

# print(sys.path)

"""
Test check_club_possibility_to_reserve_places
"""


def test_check_club_possibility_to_reserve_places_with_enough_points():
    club = {'points': 100}
    places_required = 12
    result = booking_service_srv.check_club_possibility_to_reserve_places(club, places_required)
    expected_result = True
    assert result == expected_result


def test_check_club_possibility_to_reserve_places_with_not_enough_points():
    club = {'points': 100}
    places_required = 150
    with pytest.raises(booking_service_srv.bookingError) as e:
        booking_service_srv.check_club_possibility_to_reserve_places(club, places_required)
    assert str(e.value) == "You don't have enough points. Points remaining (100)!"


def test_check_club_possibility_to_reserve_places_with_exceeded_max_allowed_places():
    club = {'points': 200}
    places_required = 100
    max_authorathed_to_reserve = 12
    with pytest.raises(booking_service_srv.bookingError) as e:
        booking_service_srv.check_club_possibility_to_reserve_places(club, places_required)

    assert str(e.value) == f"You cannot reserve more than ({max_authorathed_to_reserve}) places!"


"""
Test is_competition_in_present
"""


@freeze_time("2022-01-14")
def test_is_competition_in_present_ok():
    competition_date = "2023-01-20 13:30:00"
    result = booking_service_srv.is_competition_in_present(competition_date)
    expected_result = True
    assert result == expected_result


@freeze_time("2022-01-14")
def test_is_competition_in_present_event_in_past():
    competition_date = "2022-01-11 00:30:00"
    result = booking_service_srv.is_competition_in_present(competition_date)
    expected_result = False
    assert result == expected_result


"""
Test check_reservation_not_in_past
"""


@patch.object(booking_service_srv, 'is_competition_in_present')
def test_check_reservation_not_in_past(mock_is_competition_in_present):
    mock_is_competition_in_present.return_value = True
    competition_date = datetime(2022, 10, 22, 13, 30, 0)
    result = booking_service_srv.check_reservation_not_in_past(competition_date)
    assert result is True


@patch.object(booking_service_srv, 'is_competition_in_present')
def test_check_reservation_not_in_past_in_past(mock_is_competition_in_present):
    mock_is_competition_in_present.return_value = False
    competition_date = datetime(2022, 10, 22, 13, 30, 0)
    with pytest.raises(booking_service_srv.bookingError) as e:
        booking_service_srv.check_reservation_not_in_past(competition_date)
    assert str(e.value) == "You are not able to book a place on a post-dated competition."
