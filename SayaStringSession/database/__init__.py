import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from env import DATABASE_URL

BASE = declarative_base()


def is_supported_database_url(database_url: str) -> bool:
    driver = database_url.split(":", 1)[0].lower()
    return driver.startswith("postgresql") or driver == "sqlite"


def start():
    if not DATABASE_URL:
        print("DATABASE_URL not provided. User stats are disabled.")
        return None
    if not is_supported_database_url(DATABASE_URL):
        logging.warning("Unsupported DATABASE_URL type. User stats are disabled.")
        return None
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        BASE.metadata.bind = engine
        BASE.metadata.create_all(engine)
        return scoped_session(sessionmaker(bind=engine, autoflush=False))
    except SQLAlchemyError:
        logging.exception("Could not initialize the stats database. User stats are disabled.")
        return None


SESSION = start()
