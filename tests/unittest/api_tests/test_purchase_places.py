import os
from datetime import datetime
from http import HTTPStatus
from unittest import TestCase
from unittest.mock import patch

from assertpy import assert_that

from server import app
from services import booking_service_srv

print(os.getcwd())


class TestServerPurchasePlace(TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    @patch('server.flash')
    @patch.object(booking_service_srv, 'check_reservation_not_in_past')
    @patch.object(booking_service_srv, 'check_club_possibility_to_reserve_places')
    @patch('server.loadClubs')
    @patch('server.loadCompetitions')
    def test_purchase_places_success(
            self,
            mock_loadCompetitions,
            mock_loadClubs,
            mock_check_club_possibility_to_reserve_places,
            mock_check_reservation_not_in_past,
            mock_flash,
    ):
        # Mock a POST request with form data
        competition_date = "2025-08-31 06:28:46"
        clubs = [
            {"name": "Vidoo", "email": "gbranscombe0@google.com.hk", 'points': "15"},
            {"name": "BlogXS", "email": "truddlesden1@ow.ly", "points": "20"},
            {"name": "Miboo", "email": "lsimeons2@nydailynews.com", "points": "13"},
        ]
        competitions = [
            {"name": "Oloo", "date": competition_date, "numberOfPlaces": "30"},
            {"name": "Twitterbeat", "date": "2023-02-01 05:30:33", "numberOfPlaces": "23"},
            {"name": "Gevee", "date": "2022-09-09 08:51:55", "numberOfPlaces": "7"},
            {"name": "Divavu", "date": "2022-11-23 16:13:57", "numberOfPlaces": "15"},
            {"name": "Zoonder", "date": "2022-08-31 06:28:46", "numberOfPlaces": "20"},
        ]

        places_required = "3"
        # club = {"name": club_name, "email": "gbranscombe0@google.com.hk", 'points': "15"}
        # competition = {"name": competition_name, "date": competition_date, "numberOfPlaces": "30"}

        mock_loadCompetitions.return_value = competitions
        mock_loadClubs.return_value = clubs
        mock_check_club_possibility_to_reserve_places.return_value = True
        mock_check_reservation_not_in_past.return_value = True

        # Make a POST request to the endpoint
        payload = {
            'club': "BlogXS",
            'competition': "Oloo",
            'places': places_required
        }

        response = self.client.post('/purchasePlaces', json=payload)
        assert_that(response.status_code, HTTPStatus.OK)

    @patch('server.check_reservation_not_in_past')
    @patch('server.check_club_possibility_to_reserve_places')
    @patch('server.loadClubs')
    @patch('server.loadCompetitions')
    def test_purchase_places_booking_error(
            self,
            mock_loadCompetitions,
            mock_loadClubs,
            mock_check_club_possibility_to_reserve_places,
            mock_check_reservation_not_in_past,
    ):
        # Mock a POST request with form data
        competition_date = datetime(2025, 8, 31, 6, 28, 46)
        clubs = [
            {"name": "Vidoo", "email": "gbranscombe0@google.com.hk", 'points': "15"},
            {"name": "BlogXS", "email": "truddlesden1@ow.ly", "points": "20"},
            {"name": "Miboo", "email": "lsimeons2@nydailynews.com", "points": "13"},
        ]
        competitions = [
            {"name": "Oloo", "date": competition_date, "numberOfPlaces": "30"},
            {"name": "Twitterbeat", "date": "2023-02-01 05:30:33", "numberOfPlaces": "23"},
            {"name": "Gevee", "date": "2022-09-09 08:51:55", "numberOfPlaces": "7"},
            {"name": "Divavu", "date": "2022-11-23 16:13:57", "numberOfPlaces": "15"},
            {"name": "Zoonder", "date": "2022-08-31 06:28:46", "numberOfPlaces": "20"},
        ]
        places_required = "3"
        mock_loadCompetitions.return_value = competitions
        mock_loadClubs.return_value = clubs

        mock_check_club_possibility_to_reserve_places.return_value = False
        mock_check_reservation_not_in_past.return_value = True

        # Make a POST request to the endpoint
        payload = {
            'club': "BlogXS",
            'competition': "Oloo",
            'places': places_required
        }
        response = self.client.post('/purchasePlaces', json=payload)
        print(f"response : {response}")
        assert_that(response.status_code, HTTPStatus.BAD_REQUEST)
