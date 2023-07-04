import os
import unittest
from unittest.mock import patch
from server import app
import pytest
from assertpy import assert_that

print(os.getcwd())


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestClubsPoints(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    @patch('server.loadClubs')
    def test_clubs_points(
            self,
            mock_loadClubs,
    ):
        clubs_test = [
            {"name": "Vidoo", "email": "gbranscombe0@google.com.hk", "points": 10},
            {"name": "BlogXS", "email": "truddlesden1@ow.ly", "points": 20},
            {"name": "Miboo", "email": "lsimeons2@nydailynews.com", "points": 13},
            {"name": "Centimia", "email": "svanyakin3@phpbb.com", "points": 24},
            {"name": "Divanoodle", "email": "kelgy4@cocolog-nifty.com", "points": 15}
        ]

        mock_loadClubs.return_value = clubs_test
        # Call the endpoint directly
        response = self.client.get('/clubsPoints')
        assert_that(response.status_code).is_equal_to(200)
