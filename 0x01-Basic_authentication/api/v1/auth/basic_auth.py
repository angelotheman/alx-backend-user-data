#!/usr/bin/env python3
"""
Basic authentication module
"""
import base64
from .auth import Auth


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

        username, password = decoded_base64_authorization_header.split(':')

        return username, password
