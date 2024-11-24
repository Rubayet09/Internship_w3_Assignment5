import pytest
import jwt
from datetime import datetime, timedelta
from src.authentication_service import app, SECRET_KEY

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def create_token(email="test@example.com", role="User", expired=False):
    exp_time = datetime.now() - timedelta(hours=1) if expired else datetime.now() + timedelta(hours=1)
    payload = {
        'email': email,
        'role': role,
        'exp': exp_time.timestamp()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

class TestAuthenticationService:
    def test_verify_token_success(self, client):
        token = create_token()
        response = client.post('/auth/verify', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['valid'] == True
        assert data['user']['email'] == "test@example.com"
        assert data['user']['role'] == "User"

    def test_verify_token_missing(self, client):
        response = client.post('/auth/verify')
        assert response.status_code == 401
        assert response.get_json()['error'] == "Token is missing"

    def test_verify_token_expired(self, client):
        token = create_token(expired=True)
        response = client.post('/auth/verify', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 401
        assert response.get_json()['error'] == "Token has expired"

    def test_verify_token_invalid(self, client):
        response = client.post('/auth/verify', headers={'Authorization': 'Bearer invalid_token'})
        assert response.status_code == 401
        assert response.get_json()['error'] == "Invalid token"

    def test_check_admin_success(self, client):
        token = create_token(role="Admin")
        response = client.post('/auth/check-admin', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        assert response.get_json()['isAdmin'] == True

    def test_check_admin_not_admin(self, client):
        token = create_token(role="User")
        response = client.post('/auth/check-admin', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 403
        assert response.get_json()['error'] == "Insufficient permissions"

    def test_check_admin_missing_token(self, client):
        response = client.post('/auth/check-admin')
        assert response.status_code == 401
        assert response.get_json()['error'] == "Token is missing"