import json
from sqlalchemy import Sequence, Index
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.schema import Column, Index
from sqlalchemy.sql.sqltypes import Integer, String, DateTime

ModelBase = declarative_base()

class Client(ModelBase):
    __tablename__ = 'jwt_client'
    id = Column(Integer, Sequence('id'), primary_key=True)
    name = Column(String(255))
    client_id = Column(String(36))
    client_secret = Column(String(255))
    client_key = Column(String(255))
    create_date = Column(DateTime)
    update_date = Column(DateTime)

    Index('uq_client_id', client_id, unique=True)

    def __repr__(self):
        return ("{name: '%s', client_id: '%s', client_secret: '%s', "
                "client_key: '%s', create_date: '%s', update_date: '%s'}") % (
                    self.name, self.client_id, self.client_secret,
                    self.client_key, self.create_date, self.update_date)
