from datetime import datetime
from extensions import db


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "price": self.price,
            "release_date": (
                self.release_date.isoformat() if self.release_date else None
            ),
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
