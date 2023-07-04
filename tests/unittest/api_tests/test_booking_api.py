import unittest
from http import HTTPStatus
from unittest.mock import patch

import pytest
from assertpy import assert_that

from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestServerBooking(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    @patch('server.loadClubs')
    @patch('server.loadCompetitions')
    def test_book(self, mock_loadCompetitions, mock_loadClubs):
        # initialisation
        clubs = [
            {"name": "Vidoo", "email": "gbranscombe0@google.com.hk", "points": "10"},
            {"name": "BlogXS", "email": "truddlesden1@ow.ly", "points": "20"},
            {"name": "Miboo", "email": "lsimeons2@nydailynews.com", "points": "13"},
            {"name": "Centimia", "email": "svanyakin3@phpbb.com", "points": "24"},
            {"name": "Divanoodle", "email": "kelgy4@cocolog-nifty.com", "points": "15"}
        ]
        competitions = [
            {"name": "Dabjam", "date": "2023-02-11 22:30:33", "numberOfPlaces": "12"},
            {"name": "Quatz", "date": "2023-02-04 16:30:33", "numberOfPlaces": "10"},
            {"name": "Skyba", "date": "2023-01-01 05:00:33", "numberOfPlaces": "4"},
            {"name": "Roomm", "date": "2021-12-01 00:30:33", "numberOfPlaces": "5"},
            {"name": "Katz", "date": "2023-02-01 05:30:33", "numberOfPlaces": "27"}
        ]
        mock_loadCompetitions.side_effect = competitions
        mock_loadClubs.side_effect = clubs

        response = self.client.get('/book/Skyba/Centimia')
        assert_that(response.status_code, HTTPStatus.OK)
        mock_loadCompetitions.assrt_called_once_with()
        mock_loadClubs.assrt_called_once_with()

    @patch('server.flash')
    @patch('server.loadClubs')
    @patch('server.loadCompetitions')
    def test_book_club_not_found_error(self, mock_loadCompetitions, mock_loadClubs, mock_flash):
        clubs = [
            {"name": "Vidoo", "email": "gbranscombe0@google.com.hk", "points": 10},
            {"name": "BlogXS", "email": "truddlesden1@ow.ly", "points": 20},
            {"name": "Miboo", "email": "lsimeons2@nydailynews.com", "points": 13},
            {"name": "Centimia", "email": "svanyakin3@phpbb.com", "points": 24},
            {"name": "Divanoodle", "email": "kelgy4@cocolog-nifty.com", "points": 15}
        ]
        competitions = [
            {"name": "Dabjam", "date": "2023-02-11 22:30:33", "numberOfPlaces": 12},
            {"name": "Quatz", "date": "2023-02-04 16:30:33", "numberOfPlaces": 10},
            {"name": "Skyba", "date": "2023-01-01 05:00:33", "numberOfPlaces": 4},
            {"name": "Roomm", "date": "2021-12-01 00:30:33", "numberOfPlaces": 5},
            {"name": "Katz", "date": "2023-02-01 05:30:33", "numberOfPlaces": 27}
        ]
        mock_loadCompetitions.return_value = competitions
        mock_loadClubs.return_value = clubs
        response = self.client.get('/book/NotFoundClub/Divanoodle')
        assert response.status_code == 404
        mock_flash.assert_called_once_with("Club not found")

    @patch('server.flash')
    @patch('server.loadClubs')
    @patch('server.loadCompetitions')
    def test_book_competition_not_found_error(self, mock_loadCompetitions, mock_loadClubs, mock_flash):
        clubs = [
            {"name": "Vidoo", "email": "gbranscombe0@google.com.hk", "points": "10"},
            {"name": "BlogXS", "email": "truddlesden1@ow.ly", "points": "20"},
        ]
        competitions = [
            {"name": "Dabjam", "date": "2023-02-11 22:30:33", "numberOfPlaces": "12"},
            {"name": "Quatz", "date": "2023-02-04 16:30:33", "numberOfPlaces": "10"},
        ]
        mock_loadCompetitions.return_value = competitions
        mock_loadClubs.return_value = clubs
        response = self.client.get('/book/Vidoo/NotFoundComp')
        assert response.status_code == 404
