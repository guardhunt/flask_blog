from . import db
from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, validates
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

Base = db.Model
metadata = Base.metadata
BIT = db.Boolean
TIMESTAMP = db.TIMESTAMP


@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)


class Users(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(String())
    email = Column(String(), nullable=False)
    password = Column(String(), nullable=False)
    user_type = Column(Enum('admin', 'user'))

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        return email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    slug = Column(String())
    user_id = Column(ForeignKey('users.id'), nullable=False)
    title = Column(String())
    body = Column(String())
    published = Column(BIT())
    date_time = Column(TIMESTAMP())


class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    post_id = Column(ForeignKey('posts.id'), nullable=False)
    body = Column(String)
    date_time = Column(TIMESTAMP())




