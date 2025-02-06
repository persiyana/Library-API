"""
This module contains tests for the user registration functionality in the Flask application.
"""
import pytest
from flask import Flask
from flask_restful import Api
from models import db
from models.user_model import UserModel
from resources.register import Register


@pytest.fixture(scope='module', name="client")
def client_fixture():
    """
    Fixture to set up and provide a test client for the Flask application.

    This fixture initializes a Flask app in testing mode with an in-memory SQLite database.
    It also registers the necessary routes for the application and sets up the test client.
    The database schema is created before the tests and cleaned up after the tests.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    app.config['TESTING'] = True
    db.init_app(app)
    api = Api(app)
    api.add_resource(Register, '/api/register/')

    with app.app_context():
        db.create_all()

    yield app.test_client()

    with app.app_context():
        db.drop_all()

@pytest.fixture(name="new_user_data")
def new_user_data_fixture():
    """
    Fixture to provide data for creating a new user.

    This fixture returns a dictionary containing the necessary data for registering a new user
    (name, email, and password) that can be used in test cases.
    """
    return {
        'name': 'Test User',
        'email': 'testuser@example.com',
        'password': 'securepassword'
    }

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
