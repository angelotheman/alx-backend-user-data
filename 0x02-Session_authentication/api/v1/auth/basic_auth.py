#!/usr/bin/env python3
"""
Basic authentication module
"""
import base64
from .auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Implementing Basic Authentication
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extract the base64 authorization
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        parts = authorization_header.split(" ", 1)
        if len(parts) == 2:
            return parts[1]

        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decode base64 in authorization header
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_header = base64.b64decode(
                    base64_authorization_header, validate=True)
            return decoded_header.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract user credentials
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        username, password = decoded_base64_authorization_header.split(':', 1)

        return username, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Get's the user object from credentials given
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception as e:
            return None

        if not users:
            return None

        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current user of the session
        """
        auth_header = self.authorization_header(request)

        if auth_header is None:
            return None

        base64_header = self.extract_base64_authorization_header(auth_header)

        if base64_header is None:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)

        if decoded_header is None:
            return None

        user_email, password = self.extract_user_credentials(decoded_header)

        if user_email is None or password is None:
            return None

        return self.user_object_from_credentials(user_email, password)
