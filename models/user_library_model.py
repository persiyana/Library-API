from models import db

class UserLibraryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book_model.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    user = db.relationship('UserModel', backref=db.backref('library', lazy=True))
    book = db.relationship('BookModel', backref=db.backref('user_libraries', lazy=True))

    def __init__(self, user_id, book_id, status):
        self.user_id = user_id
        self.book_id = book_id
        self.status = status