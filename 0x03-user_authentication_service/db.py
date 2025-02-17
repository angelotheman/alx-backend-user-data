#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.session import Session

from user import Base, User


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
        Adds user to the database
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Returns the first instance of a user object
        """
        try:
            result = self._session.query(User).filter_by(**kwargs).first()

            if result:
                return result
            else:
                raise NoResultFound()
        except NoResultFound as e:
            raise e
        except InvalidRequestError as e:
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError
                setattr(user, key, value)
            self.__session.commit()
        except NoResultFound as e:
            raise e
        except Exception as e:
            self.__session.rollback()
            raise e
