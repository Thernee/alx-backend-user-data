#!/usr/bin/env python3

"""
Module for authentication
"""
from typing import TypeVar, List
from flask import request
User = TypeVar('User')


class Auth:
    """
    Manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Handle require auth"""
        return False

    def authorization_header(self, request=None) -> str:
        """
        Handle auth header
        """
        return None

    def current_user(self, request=None) -> User:
        """
        Handle user on current session
        """
        return None
