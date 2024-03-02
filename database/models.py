from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    notify_before_days = Column(Integer)
    token = Column(String)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, token={self.token}, username={self.username}, first_name={self.first_name}, last_name={self.last_name}, notify_before_days={self.notify_before_days}, created_at={self.created_at})>"
