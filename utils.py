from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_PATH

def get_engine(db_path = DB_PATH):
    return create_engine(db_path)

def get_session(engine = get_engine()):
    session = sessionmaker()
    session.configure(bind=engine)
    return session()
