#!/usr/bin/env python3
"""
Module to handle the sessions
"""
import uuid
from .auth import Auth
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """
    Class inherits from Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a new session for the current user
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        This returns a user id based on a session id
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns user based on the cookie value
        """
        if request is None:
            return None

        try:
            session_id = self.session_cookie(request)
            user_id = self.user_id_for_session_id(session_id)
            user = User.get(user_id)
        except Exception as e:
            return None

        return user

    def destroy_session(self, request=None) -> bool:
        """
        Destroys the current session
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return False

        if session_id in self.user_id_by_session:
            del self.user_id_by_session_id[session_id]
            return True

        return False
