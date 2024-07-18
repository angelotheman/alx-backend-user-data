#!/usr/bin/env python3
"""
Authenticating the database
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of input
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
