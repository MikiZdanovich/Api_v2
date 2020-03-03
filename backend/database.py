from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

session_factory = sessionmaker()

Session = scoped_session(session_factory)

engine = None
metadata = MetaData()


def configure_engine(url):
    global engine
    engine = create_engine(url)
    session_factory.configure(bind=engine)
    return engine
