"""
This module contains tests for the BookModel CRUD operations,
user authentication, and authorization.
"""
from src.models import db
from src.models.book_model import BookModel
from src.models.user_model import UserModel

def test_create_book(init_db, client, access_token):
    """
    Test case for creating a new book.
    """
    _ = init_db
    book_data = {
        'title': 'New Book',
        'author': 'New Author',
        'genre': 'Science Fiction',
        'description': 'A new test book'
    }

    response = client.post('/api/books/', json=book_data,
                           headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 201
    assert response.json['message'] == 'Book added successfully'


def test_get_book(init_db, client, access_token):
    """
    Test case for retrieving the details of a specific book.

    This test sends a GET request to the API to retrieve a book's details using its ID.
    It asserts that the book's title, author, and genre match the expected values.
    """
    _ = init_db
    book = BookModel.query.first()
    assert book is not None, "No book found in the database"

    response = client.get(f'/api/books/{book.id}/',
                          headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 200
    assert response.json['title'] == book.title
    assert response.json['author'] == book.author
    assert response.json['genre'] == book.genre

def test_update_book(init_db, client, access_token):
    """
    Test case for updating the details of an existing book.

    This test sends a PATCH request to the API to update the title, author, 
    and genre of an existing book. It asserts that the response status code 
    is 200 and that the updated book details are correctly saved.
    """
    _ = init_db
    book = BookModel.query.first()
    assert book is not None, "No book found in the database"
    update_data = {
        'title': 'Updated Book',
        'author': 'Updated Author',
        'genre': 'Mystery'
    }
    user = UserModel.query.first()
    assert user is not None, "No user found in the database"
    user.role = 'admin'
    db.session.commit()
    response = client.patch(f'/api/books/{book.id}/', json=update_data,
                            headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 200
    assert response.json['message'] == 'Book updated successfully'
    book = db.session.get(BookModel, book.id)
    assert book is not None, "No book found in the database"
    assert book.title == 'Updated Book'
    assert book.author == 'Updated Author'
    assert book.genre == 'Mystery'


def test_delete_book(init_db, client, access_token):
    """
    Test case for deleting a book.

    This test sends a DELETE request to the API to remove a specific book. 
    It asserts that the response status code is 200 and the book is deleted successfully.
    """
    _ = init_db
    user = UserModel.query.first()
    assert user is not None, "No user found in the database"
    user.role = 'admin'
    db.session.commit()

    book = BookModel.query.first()
    assert book is not None, "No book found in the database"
    response = client.delete(f'/api/books/{book.id}/',
                             headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Book deleted successfully'
    book = db.session.get(BookModel, book.id)
    assert book is None


def test_create_book_without_permission(client):
    """
    Test case for attempting to create a book without authorization.
    """
    book_data = {
        'title': 'Unauthorized Book',
        'author': 'Unauthorized Author',
        'genre': 'Drama'
    }
    response = client.post('/api/books/', json=book_data)
    assert response.status_code == 401
    assert 'Missing Authorization Header' in response.json.get('msg', '')


def test_unauthorized_user_patch(init_db, client, access_token):
    """
    Test case for an unauthorized user attempting to update a book.

    This test sends a PATCH request to update a book while the user role is not 'admin'. 
    It asserts that the server returns a 403 Forbidden error since regular users 
    cannot update books.
    """
    _ = init_db
    user = UserModel.query.first()
    assert user is not None, "No user found in the database"
    user.role = 'user'
    db.session.commit()

    book = BookModel.query.first()
    assert book is not None, "No book found in the database"

    update_data = {
        'title': 'Invalid Update',
        'author': 'Invalid Author'
    }

    response = client.patch(
        f'/api/books/{book.id}/',
        json=update_data,
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 403



def test_admin_user_patch(init_db, client, access_token):
    """
    Test case for an admin user updating a book.

    This test sends a PATCH request to update a book with an admin user. 
    It asserts that the response status code is 200 and the book is successfully updated.
    """
    _ = init_db
    user = UserModel.query.first()
    assert user is not None, "No user found in the database"
    user.role = 'admin'
    db.session.commit()

    book = BookModel.query.first()
    assert book is not None, "No book found in the database"
    update_data = {
        'title': 'Valid Update',
        'author': 'Valid Author'
    }
    response = client.patch(f'/api/books/{book.id}/', json=update_data,
                            headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Book updated successfully'


def test_user_login(init_db, client):
    """
    Test case for a successful user login.

    This test sends a POST request to the login endpoint with valid credentials. 
    It asserts that the server returns a 200 status code and includes an access 
    token in the response.
    """
    _ = init_db
    login_data = {
        'email': 'testuser@example.com',
        'password': 'password123'
    }
    response = client.post('/api/login/', json=login_data)
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_incorrect_password_login(init_db, client):
    """
    Test case for login failure due to incorrect password.

    This test sends a POST request to the login endpoint with invalid credentials. 
    It asserts that the server returns a 401 Unauthorized error and an appropriate error message.
    """
    _ = init_db
    login_data = {
        'email': 'testuser@example.com',
        'password': 'wrongpassword'
    }
    response = client.post('/api/login/', json=login_data)
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid pass'
