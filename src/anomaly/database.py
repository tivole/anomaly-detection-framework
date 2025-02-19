from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class TelemetryData(Base):
    __tablename__ = "telemetry_data"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    data = Column(Text, nullable=False)

    def __init__(self, timestamp: datetime, data: str):
        self.timestamp = timestamp
        self.data = data


def init_db(db_url: str):
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session
