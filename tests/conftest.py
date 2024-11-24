import pytest
import os
import json
from pathlib import Path

@pytest.fixture(autouse=True)
def setup_test_environment(tmp_path):
    """Set up test environment with temporary files."""
    # Create temporary JSON files
    users_file = tmp_path / "users.json"
    destinations_file = tmp_path / "destinations.json"
    
    # Initialize empty JSON files
    users_file.write_text("{}")
    destinations_file.write_text("{}")
    
    # Set environment variables
    os.environ['USER_FILE'] = str(users_file)
    os.environ['DESTINATION_FILE'] = str(destinations_file)
    os.environ['SECRET_KEY'] = 'test_secret_key'
    
    yield
    
    # Cleanup
    os.environ.pop('USER_FILE', None)
    os.environ.pop('DESTINATION_FILE', None)
    os.environ.pop('SECRET_KEY', None)