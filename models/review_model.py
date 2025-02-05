from models import db

class ReviewModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book_model.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    review_text = db.Column(db.Text, nullable=True)

    user = db.relationship('UserModel', backref=db.backref('reviews', lazy=True))
    book = db.relationship('BookModel', back_populates='reviews')

    def __init__(self, user_id, book_id, rating=None, review_text=None):
        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating
        self.review_text = review_text

    def save_review(self, rating, review_text):
        self.rating = rating
        self.review_text = review_text
        db.session.add(self) 
        db.session.commit()

        from models.book_model import BookModel  

        book = db.session.get(BookModel, self.book_id)
        if book:
            book.update_average_rating()
