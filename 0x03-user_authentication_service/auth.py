#!/usr/bin/env python3
"""
Authenticating the database
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of input
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
