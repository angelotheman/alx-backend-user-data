from datetime import datetime, timedelta
import os
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Modify the expiry
    """
    def __init__(self):
        """Overloads the init method to set session_duration."""
        super().__init__()
        self.session_duration = int(os.getenv('SESSION_DURATION', '0'))

    def create_session(self, user_id=None):
        """Overloads the create session method."""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Overloads the user_id_for_session_id
        method to handle session expiration
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict['user_id']

        if 'created_at' not in session_dict:
            return None

        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = session_dict['created_at'] + time_span
        if exp_time < cur_time:
            return None

        return session_dict['user_id']
