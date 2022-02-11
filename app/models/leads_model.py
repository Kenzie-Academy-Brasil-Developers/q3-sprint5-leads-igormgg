from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.configs.database import db

@dataclass
class Leads_Model(db.Model):
    id: int
    name: str
    email: str
    phone: str
    creation_date: str
    last_visit: str
    visits: int

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow())
    last_visit = Column(DateTime, default=datetime.utcnow())
    visits = Column(Integer, default=1)

    available_keys = ['name', 'email', 'phone']