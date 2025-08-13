from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Usage(Base):
    __tablename__ = 'usage'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
