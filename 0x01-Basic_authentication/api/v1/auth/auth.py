#!/usr/bin/env python3
"""
Authentication module for the application
"""
import re
from flask import request
<<<<<<< HEAD
from typing import List, TypeVar
=======
from typing import List
>>>>>>> 563980cd369ec9abde7186b6ac24d0415b9de2e9


class Auth:
    """
    Class to handle authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Looks for the required paths
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Authorization header function
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user logged in
        """
        return None
