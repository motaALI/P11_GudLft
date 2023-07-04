import os
import unittest
from server import app
import pytest
from assertpy import assert_that
print(os.getcwd())


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Add
class TestServer(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/')
        assert_that(response.status_code).is_equal_to(200)

    def test_show_summary(self):
        # Mock a POST request with form data
        data = {'email': 'test@example.com'}
        response = self.client.post('/showSummary', data=data)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/logout')
        assert_that(response.status_code).is_equal_to(302)
