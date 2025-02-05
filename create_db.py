from main import app, db
from models.user_model import UserModel
from models.book_model import BookModel
from models.review_model import ReviewModel
from models.user_library_model import UserLibraryModel
from werkzeug.security import generate_password_hash
import random

def create_admin_users():
    """Create multiple admin users."""
    admin_emails = [
        "admin@gmail.com",
        "superadmin@gmail.com",
        "libraryadmin@gmail.com",
        "moderator@gmail.com",
        "manager@gmail.com",
    ]

    for email in admin_emails:
        existing_admin = UserModel.query.filter_by(email=email).first()
        if not existing_admin:
            admin_user = UserModel(
                name=email.split("@")[0].capitalize(),
                email=email,
                password="admin123",
                role="admin"
            )
            db.session.add(admin_user)

    db.session.commit()

def create_users():
    """Create multiple regular users."""
    users = [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": "bob@example.com"},
        {"name": "Charlie", "email": "charlie@example.com"},
        {"name": "David", "email": "david@example.com"},
        {"name": "Eve", "email": "eve@example.com"},
        {"name": "Frank", "email": "frank@example.com"},
        {"name": "Grace", "email": "grace@example.com"},
        {"name": "Hank", "email": "hank@example.com"},
        {"name": "Ivy", "email": "ivy@example.com"},
        {"name": "Jack", "email": "jack@example.com"},
    ]

    for user in users:
        existing_user = UserModel.query.filter_by(email=user["email"]).first()
        if not existing_user:
            new_user = UserModel(
                name=user["name"],
                email=user["email"],
                password="password123",
                role="user"
            )
            db.session.add(new_user)

    db.session.commit()

def create_books():
    """Create multiple books."""
    book_data = [
        ("The Great Gatsby", "F. Scott Fitzgerald", "Fiction"),
        ("1984", "George Orwell", "Dystopian"),
        ("To Kill a Mockingbird", "Harper Lee", "Classic"),
        ("The Hobbit", "J.R.R. Tolkien", "Fantasy"),
        ("The Catcher in the Rye", "J.D. Salinger", "Classic"),
        ("Moby Dick", "Herman Melville", "Adventure"),
        ("Pride and Prejudice", "Jane Austen", "Romance"),
        ("War and Peace", "Leo Tolstoy", "Historical"),
        ("Crime and Punishment", "Fyodor Dostoevsky", "Psychological"),
        ("Brave New World", "Aldous Huxley", "Dystopian"),
        ("The Shining", "Stephen King", "Horror"),
        ("Dune", "Frank Herbert", "Science Fiction"),
        ("The Alchemist", "Paulo Coelho", "Philosophical"),
        ("The Road", "Cormac McCarthy", "Post-Apocalyptic"),
        ("Les Misérables", "Victor Hugo", "Historical"),
        ("Frankenstein", "Mary Shelley", "Gothic"),
        ("Dracula", "Bram Stoker", "Horror"),
        ("The Name of the Wind", "Patrick Rothfuss", "Fantasy"),
        ("Good Omens", "Neil Gaiman & Terry Pratchett", "Comedy"),
        ("The Art of War", "Sun Tzu", "Strategy"),
        ("The Silent Patient", "Alex Michaelides", "Thriller"),
        ("The Night Circus", "Erin Morgenstern", "Magical Realism"),
        ("The Girl with the Dragon Tattoo", "Stieg Larsson", "Mystery"),
        ("The Pillars of the Earth", "Ken Follett", "Historical Fiction"),
        ("Hyperion", "Dan Simmons", "Science Fiction"),
        ("Sapiens: A Brief History of Humankind", "Yuval Noah Harari", "Non-Fiction"),
        ("Educated", "Tara Westover", "Memoir"),
        ("The Book Thief", "Markus Zusak", "Young Adult"),
        ("Maus", "Art Spiegelman", "Graphic Novel"),
        ("And Then There Were None", "Agatha Christie", "Mystery"),
        ("The Three-Body Problem", "Liu Cixin", "Hard Science Fiction"),
        ("Norwegian Wood", "Haruki Murakami", "Contemporary"),
        ("A Brief History of Time", "Stephen Hawking", "Science"),
        ("The Martian", "Andy Weir", "Science Fiction"),
        ("Circe", "Madeline Miller", "Mythology"),
        ("The House of the Spirits", "Isabel Allende", "Magical Realism"),
        ("American Gods", "Neil Gaiman", "Urban Fantasy"),
        ("The Call of the Wild", "Jack London", "Adventure"),
        ("The Kite Runner", "Khaled Hosseini", "Drama"),
        ("The Handmaid's Tale", "Margaret Atwood", "Speculative Fiction"),
        ("Guns, Germs, and Steel", "Jared Diamond", "Anthropology"),
        ("The Subtle Art of Not Giving a F*ck", "Mark Manson", "Self-Help"),
        ("Born a Crime", "Trevor Noah", "Autobiography"),
        ("Atomic Habits", "James Clear", "Self-Improvement"),
        ("The War of Art", "Steven Pressfield", "Creativity"),
        ("The Shadow of the Wind", "Carlos Ruiz Zafón", "Gothic Mystery"),
        ("The Overstory", "Richard Powers", "Eco-Fiction"),
        ("Project Hail Mary", "Andy Weir", "Science Fiction"),
        ("The Seven Husbands of Evelyn Hugo", "Taylor Jenkins Reid", "Historical Drama"),
        ("My Year of Rest and Relaxation", "Ottessa Moshfegh", "Literary Fiction"),
    ]

    for title, author, genre in book_data:
        existing_book = BookModel.query.filter_by(title=title, author=author).first()
        if not existing_book:
            new_book = BookModel(
                title=title,
                author=author,
                genre=genre,
                description=f"A compelling story by {author} in the {genre} genre."
            )
            db.session.add(new_book)

    db.session.commit()

def create_reviews():
    """Create multiple reviews for books."""
    users = UserModel.query.all()
    books = BookModel.query.all()

    review_texts = [
        "Amazing read! Highly recommend.",
        "Interesting book, but a bit slow in some parts.",
        "A masterpiece! One of the best books ever.",
        "I didn't enjoy it as much as I expected.",
        "A thought-provoking and insightful book.",
        "This book changed my perspective on life.",
        "I struggled to finish it, but the ending was great.",
        "The storytelling is brilliant!",
    ]

    for book in books:
        for user in random.sample(users, k=random.randint(2, 5)):
            rating = random.randint(1, 5)
            review_text = random.choice(review_texts)

            existing_review = ReviewModel.query.filter_by(user_id=user.id, book_id=book.id).first()
            if not existing_review:
                new_review = ReviewModel(user_id=user.id, book_id=book.id, rating=rating, review_text=review_text)
                db.session.add(new_review)

    db.session.commit()
    for book in books:
        book.update_average_rating()


def create_user_libraries():
    """Create user libraries with reading statuses."""
    users = UserModel.query.all()
    books = BookModel.query.all()
    statuses = ["reading", "completed", "wishlist"]

    for user in users:
        for book in random.sample(books, k=random.randint(3, 7)):
            status = random.choice(statuses)

            existing_entry = UserLibraryModel.query.filter_by(user_id=user.id, book_id=book.id).first()
            if not existing_entry:
                new_entry = UserLibraryModel(user_id=user.id, book_id=book.id, status=status)
                db.session.add(new_entry)

    db.session.commit()

with app.app_context():
    db.create_all()
    create_admin_users()
    create_users()
    create_books()
    create_reviews()
    create_user_libraries()
