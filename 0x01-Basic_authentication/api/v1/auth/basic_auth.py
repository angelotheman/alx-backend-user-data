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
