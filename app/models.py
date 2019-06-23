from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date
from utils.database import database_connection


Base = declarative_base()


class Customer(Base):

    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    dob = Column(Date)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow(),
        onupdate=datetime.utcnow())


if __name__ == "__main__":
    Base.metadata.drop_all(database_connection)
    Base.metadata.create_all(database_connection)
