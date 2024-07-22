#!/usr/bin/env python3
"""
Authentication module for the application
"""
import re
from os import getenv
from flask import request
from typing import List, TypeVar
from typing import List


class Auth:
    """
    Class to handle authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Looks for the required paths
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        normalized_path = path.rstrip('/')

        for excluded in excluded_paths:
            normalized_excluded = excluded.rstrip('/')
            pattern = re.sub(r'\*$', '.*', normalized_excluded)

            if re.match(pattern, normalized_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Authorization header function
        """
        if request is None:
            return None

        if "Authorization" not in request.headers:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user logged in
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Returns the cookie value from a request
        """
        if request is None:
            return None

        session_name = getenv('SESSION_NAME', '_my_session_id')

        session_id = request.cookies.get(session_name)

        return session_id
