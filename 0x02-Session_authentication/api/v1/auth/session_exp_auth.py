#!/usr/bin/env python3
"""
Module to add expiry to authentication
"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """
    Modify the expiry
    """
    def __init__(self):
        """
        Initialzes the class
        """
        super().__init__()
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """
        Overloading the create session
        """
        session_id = super().create_session(user_id)

        if not session_id:
            return None

        session_dictionary = {
                "user_id": user_id,
                "created_id": datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Overloads the user id for session id
        """
        if session_id is None:
            return None

        session_data = self.user_id_by_session.get(session_id)

        if session_data is None:
            return None

        if self.session_duration <= 0:
            return session_data.get("user_id")

        created_at = session_data.get("created_at")

        if created_at is None:
            return None

        if created_at + timedelta(seconds=self.session_duration) \
                < datetime.now():
            return None

        return session_data.get("user_id")
