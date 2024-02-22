#!/usr/bin/env python3

"""
module for user auth
"""
import bcrypt
from db import DB
from user import User
import uuid

from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hash a given password string
    """
    salted = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salted)


def _generate_uuid() -> str:
    """
    return a string representation of a new UUID
    """
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """
        Create new session for given user
        """
        try:
            user = self._db.find_user_by(email=email)
            new_uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=new_uuid)
            return new_uuid
        except Exception:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get user based on session id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Updates current user session to None
        """
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(user_id=user_id)
            self._db.update_user(user.id, session_id=None)
            return None
        except Exception:
            return None
