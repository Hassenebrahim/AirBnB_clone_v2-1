#!/usr/bin/python3

"""This is the db storage class for AirBnB"""
import imp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.base_model import Base, BaseModel
from os import getenv


class DBStorage:
    """
    Database Engine for AirBnB project
    """
    __engine = None
    __session = None

    def __init__(self):
        """Init method"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Query all object from current Database"""
        classes = {
                    'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        dict = {}
        if cls is None:
            for k, v in classes.items():
                objects = self.__session.query(v).all()
                if len(objects) > 0:
                    for obj in objects:
                        key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                        dict[key] = obj
            return dict
        else:
            if cls in classes.values():
                for obj in self.__session.query(cls).all():
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    dict[key] = obj
            return dict

    def new(self, obj):
        """add the object to the current
        database session(self.__session)"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current
        database session (self.__session)"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current
        database session(self.__session)"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables and the current database
        session(self.__session)"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
