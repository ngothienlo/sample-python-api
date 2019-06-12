from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date


Base = declarative_base()
DB_URI = 'postgresql+psycopg2:'\
         '//assign_user:assign_123@localhost/assignment_api'

# postgres is your username in assign_user. assign_123 is the password.


class Customer(Base):

    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    dob = Column(Date)
    updated_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now())


if __name__ == "__main__":
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
