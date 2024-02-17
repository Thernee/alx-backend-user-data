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
        new_path = ''
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if not path.endswith('/'):
            new_path = path + '/'
        if new_path in excluded_paths or path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Handle auth header
        """
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> User:
        """
        Handle user on current session
        """
        return None
