#!/usr/bin/env python3

"""
module for user auth
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash a given password string
    """
    salted = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salted)
