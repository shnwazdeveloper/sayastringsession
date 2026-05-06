from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from env import DATABASE_URL

BASE = declarative_base()


def start():
    if not DATABASE_URL:
        print("DATABASE_URL not provided. User stats are disabled.")
        return None
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


SESSION = start()
