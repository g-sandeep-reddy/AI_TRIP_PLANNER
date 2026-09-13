from sqlalchemy import Column, Integer, String

from database.connection import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False, index=True)

    email = Column(String, unique=True, nullable=False, index=True)

    password_hash = Column(String, nullable=False)

class Trip(Base):

    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, nullable=False)

    destination = Column(String, nullable=False)

    days = Column(Integer, nullable=False)

    budget = Column(Integer, nullable=False)

    interests = Column(String, nullable=False)

    trip_plan = Column(String, nullable=False)

class ChatSession(Base):

    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, nullable=False)

    title = Column(String, nullable=False)


class ChatMessage(Base):

    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, nullable=False)

    role = Column(String, nullable=False)

    message = Column(String, nullable=False)