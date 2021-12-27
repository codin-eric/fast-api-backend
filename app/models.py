from sqlalchemy import Column, TIMESTAMP, String, Integer, Float

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

from app.cfg import DB_CONNSTR

print(DB_CONNSTR)
engine = create_engine(DB_CONNSTR) if DB_CONNSTR else None
meta = MetaData(engine)
Base = declarative_base(metadata=meta)

TABLE_NAME = 'analytics'


class Analytics(Base):
    __tablename__ = TABLE_NAME

    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(TIMESTAMP, nullable=False)
    channel = Column(String, nullable=False)
    country = Column(String, nullable=False)
    os = Column(String, nullable=False)
    impressions = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    installs = Column(Integer, nullable=False)
    spend = Column(Float, nullable=False)
    revenue = Column(Float, nullable=False)