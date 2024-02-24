#!/usr/bin/env python3

"""
Module for session auth
"""
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    Session auth class
    """
    pass
    # validate if everything inherits correctly without any overloading
    # validate the “switch” by using environment variables

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
