from models import db
from models.review_model import ReviewModel

class BookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    average_rating = db.Column(db.Float, default=0.0)
    reviews = db.relationship('ReviewModel', back_populates='book', lazy=True)

    def __init__(self, title, author, genre, description=None, average_rating=0.0):
        self.title = title
        self.author = author
        self.genre = genre
        self.description = description
        self.average_rating = average_rating


    def update_average_rating(self):
        reviews = ReviewModel.query.filter_by(book_id=self.id).all()
        ratings = [review.rating for review in reviews if review.rating is not None]
        self.average_rating = sum(ratings) / len(ratings) if ratings else 0.0
        db.session.commit()

    @classmethod
    def search_books(cls, title=None, author=None, genre=None):
        query = cls.query
        if title:
            query = query.filter(cls.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(cls.author.ilike(f"%{author}%"))
        if genre:
            query = query.filter(cls.genre.ilike(f"%{genre}%"))
        return query.all()