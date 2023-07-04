import os
from server import app
import server
import pytest
from assertpy import assert_that

print(os.getcwd())


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestIntegration:

    @classmethod
    def setup_class(cls):
        cls.competition = [
            {
                "name": "Test",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25"
            }
        ]

        cls.club = [
            {
                "name": "Test club",
                "email": "test@example.com",
                "points": "10"
            }
        ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club

    def test_index(self, client):
        response = client.get('/')
        assert_that(response.status_code).is_equal_to(200)

    def test_show_summary(self, client):
        response = client.post('/showSummary', data={'email': 'example@example.com'})
        assert_that(response.status_code).is_equal_to(200)
        # Add additional assertions as needed

    def test_book(self, client):
        response = client.get('/book/Test/Test club')
        assert_that(response.status_code).is_equal_to(200)
        # Add additional assertions as needed

    def test_purchase_places(self, client):
        response = client.post('/purchasePlaces', data={
            'competition': 'Test',
            'club': 'Test club',
            'places': '5'
        })
        assert_that(response.status_code).is_equal_to(200)
        # Add additional assertions as needed

    def test_clubs_points(self, client):
        response = client.get('/clubsPoints')
        assert_that(response.status_code).is_equal_to(200)
        # Add additional assertions as needed

    def test_logout(self, client):
        response = client.get('/logout')
        assert_that(response.status_code).is_equal_to(302)
