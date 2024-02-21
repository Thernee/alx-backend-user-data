#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Save user to db
        """
        if email and hashed_password:
            user = User(email=email, hashed_password=hashed_password)
            # new_session = self.__session
            self._session.add(user)
            self._session.commit()
            return user
        return

    def find_user_by(self, **kwargs) -> User:
        """
        find user by given filters
        """
        try:
            results = self.__session.query(User).filter_by(**kwargs).first()
        except InvalidRequestError:
            raise InvalidRequestError
        if not results:
            raise NoResultFound
        return results

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update given user details
        """
        user = self.find_user_by(id=user_id)
        try:
            for key, value in kwargs.items():
                setattr(user, key, value)
        except Exception:
            raise ValueError
        self.__session.commit()
