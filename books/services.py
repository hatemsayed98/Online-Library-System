from .models import Book
from extensions import db


class BookService:
    def create_book(self, data):
        book = Book(title=data["title"], author=data["author"], price=data["price"])
        db.session.add(book)
        db.session.commit()
        return book

    def get_all_books(self):
        return Book.query.all()

    def get_book_by_id(self, id):
        return Book.query.filter_by(id=id).first()

    def update_book(self, book_id, update_data):
        book = self.get_book_by_id(book_id)
        if not book:
            return None

        valid_fields = {"title", "price", "author"}
        updates = {}
        if not update_data:
            return book
        for field, value in update_data.items():
            if field not in valid_fields:
                raise ValueError(f"Invalid field for update: {field}")
            if value is not None:
                updates[field] = value

        try:
            for field, value in updates.items():
                setattr(book, field, value)

            db.session.commit()
            return book
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to update book: {str(e)}")

    def delete_book(self, book_id):

        book = self.get_book_by_id(book_id)
        if not book:
            return False

        db.session.delete(book)
        db.session.commit()
        return True
