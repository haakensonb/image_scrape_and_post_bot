from utils import get_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()

class ImgRecord(Base):
    __tablename__ = 'img_record'
    id = Column(String, primary_key=True)

engine = get_engine()
Base.metadata.create_all(engine)