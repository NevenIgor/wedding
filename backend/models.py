from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    will_attend = Column(Boolean, nullable=False)
    drink_preference = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DrinkPreference(Base):
    __tablename__ = "drink_preferences"

    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, index=True)
    preference = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
