"""
This module contains tests for the user registration functionality in the Flask application.
"""
from src.models.user_model import UserModel

def test_register_user_success(client, new_user_data):
    """Test registering a user successfully."""
    response = client.post('/api/register/', json=new_user_data)

    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'

    with client.application.app_context():
        user = UserModel.query.filter_by(email=new_user_data['email']).first()
        assert user is not None
        assert user.name == new_user_data['name']
        assert user.email == new_user_data['email']

def test_register_user_email_taken(client, new_user_data):
    """Test trying to register a user with an already taken email."""
    client.post('/api/register/', json=new_user_data)

    response = client.post('/api/register/', json=new_user_data)

    assert response.status_code == 400
    assert response.json['message'] == 'Email already registered'
