import unittest
import json
import jwt
from datetime import datetime, timedelta
from src.user_service import app, validate_email, validate_password, users, save_data, USER_FILE, SECRET_KEY
from werkzeug.security import generate_password_hash
import os
SECRET_KEY = 'your_secret_key_here'

class TestUserService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.client = app.test_client()
        
        # Create a test user
        cls.test_users = {
            "test@example.com": {
                "name": "Test User",
                "email": "test@example.com",
                "password": generate_password_hash("password123"),
                "role": "Admin"
            }
        }
        with open(USER_FILE, 'w') as f:
            json.dump(cls.test_users, f)
    
    @classmethod
    def tearDownClass(cls):
        if os.path.exists(USER_FILE):
            os.remove(USER_FILE)

    def generate_token(self, email="test@example.com", role="Admin"):
        token = jwt.encode({
            'email': email,
            'role': role,
            'exp': datetime.now() + timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        return f'Bearer {token}'

    def test_register_success(self):
        data = {
            "name": "New User",
            "email": "new_user@example.com",
            "password": "password123",
            "role": "User"
        }
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], "New User")

    def test_login_success(self):
        # First register a test user
        register_data = {
            "name": "Login Test",
            "email": "login@test.com",
            "password": "password123",
            "role": "User"
        }
        self.client.post('/register', json=register_data)
        
        # Then try to login
        login_data = {
            "email": "login@test.com",
            "password": "password123"
        }
        response = self.client.post('/login', json=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.get_json())

    def test_get_profile_success(self):
        # Try to access profile with admin token
        token = self.generate_token()
        response = self.client.get(
            '/profile/test@example.com',  # Fixed: Using the correct test email
            headers={"Authorization": token}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], "Test User")

    def test_get_profile_unauthorized(self):
        # Try to access profile with non-admin token
        token = self.generate_token(email="user@test.com", role="User")
        response = self.client.get(
            '/profile/test@example.com',
            headers={"Authorization": token}
        )
        self.assertEqual(response.status_code, 403)

    def test_get_profile_not_found(self):
        token = self.generate_token()
        response = self.client.get(
            '/profile/nonexistent@example.com',
            headers={"Authorization": token}
        )
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()