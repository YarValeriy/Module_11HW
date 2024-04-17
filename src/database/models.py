from sqlalchemy import Column, Integer, String, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    birthday = Column(Date)
    additional_data = Column(String, nullable=True)
    created_at = Column('created_at', DateTime, default=func.now())
