#!/usr/bin/env python3
"""
Authenticating the database
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a user
        """
        try:
            user = self._db.find_user_by(email=email)
            return _check_password(password, user.hashed_password)
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """
        Generates a uniq ID for the instance
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
        Creates session with unique ID
        """
        user = self._db.find_user_by(email=email)
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(
            self, session_id: Optional[str]) -> Optional[User]:
        """
        Gets the user from session or none
        """
        if session_id is None:
            return None

        user = self._db.find_user_by(session_id=session_id)

        return user if user else None


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of input
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _check_password(password: str, hashed_password: bytes) -> bool:
    """
    Returns the status of a password
    """
    return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password
    )
