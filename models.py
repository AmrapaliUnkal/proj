from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

class Room(Base):
    __tablename__ = "rooms"
    room_number = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)

class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_number = Column(Integer, ForeignKey("rooms.room_number"))
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    total_amount = Column(Float, nullable=False)
    user = relationship("User")
    room = relationship("Room")

class BookingHistory(Base):
    __tablename__ = "bookings_history"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer)
    user_id = Column(Integer)
    room_number = Column(Integer)
    stay_duration = Column(Integer)
    total_amount = Column(Float)
