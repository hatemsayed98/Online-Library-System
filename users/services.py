from .models import User
from extensions import db


class UserService:
    def create_user(self, name, email, password):
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
