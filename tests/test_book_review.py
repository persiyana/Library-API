"""
This module contains tests for the review functionality in the application, 
focusing on adding reviews to books. It ensures that reviews can be added, 
validated, and managed correctly.
"""
from flask_jwt_extended import create_access_token

def test_add_review_success(client, create_user, create_book):
    """Test adding a valid review."""
    access_token = create_access_token(identity=create_user.id)
    response = client.post(
        f'/api/books/{create_book.id}/review/',
        json={'rating': 5, 'review_text': 'Excellent book!'},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 201
    assert response.json == {'message': 'Review added successfully'}

def test_add_review_invalid_rating(client, create_user, create_book):
    """Test adding a review with an invalid rating (less than 1)."""
    access_token = create_access_token(identity=create_user.id)
    response = client.post(
        f'/api/books/{create_book.id}/review/',
        json={'rating': 0, 'review_text': 'Not good!'},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 400
    assert response.json == {'message': 'Rating must be between 1 and 5'}

def test_add_review_already_reviewed(client, create_user, create_book, create_review):
    """Test when the user has already reviewed the book."""
    _ = create_review
    access_token = create_access_token(identity=create_user.id)
    response = client.post(
        f'/api/books/{create_book.id}/review/',
        json={'rating': 3, 'review_text': 'Changed my mind!'},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 400
    assert response.json == {'message': 'You have already reviewed this book'}

def test_add_review_book_not_found(client, create_user):
    """Test adding a review when the book is not found."""
    access_token = create_access_token(identity=create_user.id)
    response = client.post(
        '/api/books/999999/review/',
        json={'rating': 4, 'review_text': 'Not bad.'},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 404
    assert response.json == {'message': 'Book not found'}
