#!/usr/bin/env python3
"""
Authentication module for the application
"""
import re
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
            if normalized_excluded == normalized_path:
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

        return request["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user logged in
        """
        return None
