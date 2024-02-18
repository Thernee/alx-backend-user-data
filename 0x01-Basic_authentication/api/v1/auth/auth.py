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

# improve to allow * at the end of excluded_paths
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Require authentication
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if not path.endswith('/'):
            new_path = path + '/*'
        if path in excluded_paths or new_path in excluded_paths:
            return False
        for paths in excluded_paths:
            if paths.endswith('*') and paths[:-1] in path:
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
