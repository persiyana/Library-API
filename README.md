# Library API
A web application with REST API for managing a personal book library. It has the following functionality:
### Users:
* Registration with email and password
* Every user can:
  * Add books to your personal library by selecting one of the following categories:
    * "reading"
    * "completed"
    * "wishlist"
  * Move books between categories:
    * from "wishlist" to "completed"
    * from "completed" to "reading"
    * from "wishlist" to "reading"
  * Remove books from your personal library
  * Rate books with a rating from 1 to 5 stars
  * Add reviews to books
  * Add books
  * Search for books by title, author, or genre
  * View ratings and reviews of books by other users
### Admins:
* They have the same rights as users 
* Delete books from the database
* Edit the book details
### Books:
* Each book will contain the following attributes: title, author, genre and short description, list of reviews, rating
## Setup
1. Download the source code
2. Make .env file in which you should put `JWT_SECRET_KEY=your-secret-key` where you should generate a secret key from a site like [that one](https://jwtsecret.com/generate)
2. Create virtual enviroment `py -m venv .venv`
3. Activate the virtual enviroment `.venv/Scripts/Activate.ps1`
4. Install the requirements `pip install -r requirements.txt`
5. Create the database `py create_db.py`
6. Run the program `py main.py`
## Example usage
### You should test the program by a platform for using API for example Postman
After running the code open Postman
### Login - POST http://localhost:5000/api/login
- as an admin 
```
{
  "email": "admin@gmail.com",
  "password": "admin123"
}
```
- as a normal user
```
{
  "email": "bob@example.com",
  "password": "password123"
}
```
### Register - POST http://localhost:5000/api/register
```
{
  "name": "Ivan Ivanov",
  "email": "ivan@gmail.com",
  "password": "vankata123"
}
```
### ! For any other command you should copy the access token which is the result of the login then go to the headers section and the key should be 'Authorization' and value 'Bearer the-access-token'
### See your profile - GET http://localhost:5000/api/profile
### Get list of all books - GET http://localhost:5000/api/books
### Get info for a book + reviews - GET http://localhost:5000/api/books/{book_id}
### Search by title, author or genre - GET http://localhost:5000/api/books/?title=some title&author=some author
### Add new book - POST http://localhost:5000/api/books/
```
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "genre": "Fiction",
  "description": "A classic novel set in the 1920s."
}
```
### Add review or rating to a book - POST http://localhost:5000/api/books/{book_id}/review/
```
{
  "rating": 4,
  "review_text": "A fantastic read! Loved the characters and plot."
}
```
### See their library contents - GET  http://localhost:5000/api/library/
### Add book to their library - POST http://localhost:5000/api/library/ 
status can be completed, wishlist or reading
```
{
  "book_id": 1,
  "status": "completed"
}
```
### Change the status of their books - PATCH http://localhost:5000/api/library/{book_id}
status can be completed, wishlist or reading
```
{
  "new_status": "reading"
}
```
### Delete book from library - DELETE http://localhost:5000/api/library/{book_id}
## Available only for admins:
### Make normal user admin - POST http://localhost:5000/api/promote-to-admin
```
{
  "email": "ivan@gmail.com"
}
```
### Edit books - PATCH http://localhost:5000/api/books/{book_id}
```
{
  "title": "Updated Book Title",
  "author": "Updated Author",
  "genre": "Fiction",
  "description": "An updated description for the book."
}
```
```
{
  "author": "Other Updated Author"
}
```
### Delete books - Delete http://localhost:5000/api/books/{book_id}