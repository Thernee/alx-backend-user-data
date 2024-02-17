#!/usr/bin/env python3

"""Module for authentication"""
from typing import TypeVar
from flask import request


class Auth:
    """Manage API authentication"""
    def require_auth(self, path: str, excluded_paths: list[str]) -> bool:
        """Handle require auth"""
        return False

    def authorization_header(self, request=None) -> str:
        """Handle auth header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Handle user on current session"""
        return None
