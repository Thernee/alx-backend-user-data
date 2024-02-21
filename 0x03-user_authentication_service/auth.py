#!/usr/bin/env python3

"""
module for user auth
"""
import bcrypt
from db import DB
from user import User

from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hash a given password string
    """
    salted = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salted)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """New auth instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Verify user credentials for login
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except Exception:
            return False
        return False
