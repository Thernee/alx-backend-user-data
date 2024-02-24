#!/usr/bin/env python3

"""
Module for session auth
"""
from .auth import Auth


class SessionAuth(Auth):
    """
    Session auth class
    """

    # def create_session(self, user_id: str = None) -> str:
    #     """
    #     Create session
    #     """
    #     if user_id is None:
    #         return None
    #     if type(user_id) is not str:
    #         return None
    #     session_id = self._generate_uuid()
    #     self.user_id_by_session_id[session_id] = user_id
    #     return session_id
