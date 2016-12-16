from config import loader
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

sessmaker = sessionmaker(autoflush=True, autocommit=False)

class DbConfiguration(object):
    @classmethod
    def newsession(cls, engine):
        sessmaker = sessionmaker(autoflush=True, autocommit=False)
        dbsession = scoped_session(sessmaker)
        dbsession.configure(bind=engine)
        return dbsession

    @classmethod
    def get_service_config(cls, servicename):
        db_url = loader.ConfigLoader().current()['databases'][servicename][
            'db_url']
        db_pool_size = loader.ConfigLoader().current()['databases'][
            servicename]['pool']['pool_size']

        return (db_url, db_pool_size)

    @classmethod
    def getengine(cls, db_url, db_pool_size):
        engine = create_engine(db_url, pool_size=db_pool_size, echo=False)
        return engine
