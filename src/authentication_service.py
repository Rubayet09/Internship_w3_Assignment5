import os
import json
from flask import Flask, request, jsonify
from flasgger import Swagger
from werkzeug.exceptions import Unauthorized
import jwt
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

# Swagger Configuration
template = {
    "swagger": "2.0",
    "info": {
        "title": "Authentication Service API",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

swagger = Swagger(app, template=template)

# Secret key for JWT
SECRET_KEY = 'your_secret_key_here'

@app.route('/auth/verify', methods=['POST'])
def verify_token():
    """
    Verify JWT token and return user information
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
    responses:
      200:
        description: Token is valid
      401:
        description: Invalid or expired token
    """
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token is missing"}), 401
    
    try:
        # Extract the token from the Authorization header
        token = token.split(' ')[1] if ' ' in token else token
        
        # Decode the token without verifying expiration for now
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})

        # Debugging: Print the decoded token payload to check expiration
        print(f"Decoded token payload: {decoded}")
        
        # Manually check for expiration
        if datetime.now() > datetime.fromtimestamp(decoded['exp']):
            return jsonify({"error": "Token has expired"}), 401

        # Return user data if token is valid
        return jsonify({
            "valid": True,
            "user": {
                "email": decoded['email'],
                "role": decoded['role']
            }
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

@app.route('/auth/check-admin', methods=['POST'])
def check_admin():
    """
    Verify if token belongs to an admin user
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
    responses:
      200:
        description: User is admin
      403:
        description: User is not admin
      401:
        description: Invalid token
    """
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token is missing"}), 401
    
    try:
        # Extract the token from the Authorization header
        token = token.split(' ')[1] if ' ' in token else token
        
        # Decode the token
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        # Check if the user has admin role
        if decoded['role'] != 'Admin':
            return jsonify({"error": "Insufficient permissions"}), 403
        return jsonify({"isAdmin": True}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == '__main__':
    app.run(port=5003, debug=True)
