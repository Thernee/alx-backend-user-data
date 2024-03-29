#!/usr/bin/env python3

"""
Module for BasicAuth
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    BasicAuth class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Return the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_b64_auth_header: str) -> (str, str):
        """
        Return the user email and password from the Base64 decoded value
        """
        if decoded_b64_auth_header is None:
            return (None, None)
        if type(decoded_b64_auth_header) is not str:
            return (None, None)
        if ":" not in decoded_b64_auth_header:
            return (None, None)
        data = decoded_b64_auth_header.split(':', 1)
        return (data[0], data[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Return the User instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        if len(user) == 0:
            return None
        user = user[0]
        if user.is_valid_password(user_pwd):
            return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return the User instance for a request
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        if base64_auth_header is None:
            return None
        decoded_b64_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        if decoded_b64_auth_header is None:
            return None
        email, password = self.extract_user_credentials(
            decoded_b64_auth_header)
        if email is None or password is None:
            return None
        user = self.user_object_from_credentials(email, password)
        return user
