import pytest
import json
from unittest.mock import patch, mock_open
from src.destination_service import app, destinations, save_data

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_destinations():
    return {
        "1": {
            "id": "1",
            "name": "Paris",
            "description": "City of Light",
            "location": "France"
        }
    }

@pytest.fixture
def mock_auth_response(requests_mock):
    requests_mock.post('http://localhost:5003/auth/verify', json={'valid': True})
    requests_mock.post('http://localhost:5003/auth/check-admin', json={'isAdmin': True})

class TestDestinationService:
    def test_get_destinations(self, client, mock_destinations):
        with patch.dict(destinations, mock_destinations, clear=True):
            response = client.get('/destinations')
            assert response.status_code == 200
            assert len(response.get_json()) == 1
            assert response.get_json()[0]['name'] == 'Paris'

    def test_add_destination_success(self, client, mock_auth_response):
        new_destination = {
            "name": "London",
            "description": "Big Ben",
            "location": "UK"
        }
        with patch('src.destination_service.save_data') as mock_save:
            response = client.post(
                '/destinations',
                json=new_destination,
                headers={'Authorization': 'Bearer valid_token'}
            )
            assert response.status_code == 201
            assert response.get_json()['name'] == 'London'
            mock_save.assert_called_once()

    def test_add_destination_missing_fields(self, client, mock_auth_response):
        response = client.post(
            '/destinations',
            json={"name": "London"},
            headers={'Authorization': 'Bearer valid_token'}
        )
        assert response.status_code == 400
        assert 'Missing required fields' in response.get_json()['error']

    def test_add_destination_duplicate_name(self, client, mock_destinations, mock_auth_response):
        with patch.dict(destinations, mock_destinations, clear=True):
            response = client.post(
                '/destinations',
                json={
                    "name": "Paris",
                    "description": "Another Paris",
                    "location": "USA"
                },
                headers={'Authorization': 'Bearer valid_token'}
            )
            assert response.status_code == 400
            assert 'already exists' in response.get_json()['error']

    def test_delete_destination_success(self, client, mock_destinations, mock_auth_response):
        with patch.dict(destinations, mock_destinations, clear=True):
            with patch('src.destination_service.save_data') as mock_save:
                response = client.delete(
                    '/destinations/1',
                    headers={'Authorization': 'Bearer valid_token'}
                )
                assert response.status_code == 200
                assert 'Destination deleted successfully' in response.get_json()['message']
                mock_save.assert_called_once()

    def test_delete_destination_not_found(self, client, mock_auth_response):
        response = client.delete(
            '/destinations/999',
            headers={'Authorization': 'Bearer valid_token'}
        )
        assert response.status_code == 404
        assert 'Destination not found' in response.get_json()['error']