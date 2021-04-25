from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    JSON,
    DateTime,
    Float, Text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random


Base = declarative_base()
engine = create_engine("sqlite:///bible.db", echo = True)


class User(Base):
    __tablename__ = "users"

    uid = Column("uid", Integer, primary_key=True)
    username = Column("username", String, unique=True)
    password = Column("password", String)
    email = Column("email", String)


class Review(Base):
    __tablename__ = "reviews"

    rid = Column("rid", Integer, primary_key=True)
    publicity = Column("publicity", Boolean)
    teacher = Column("teacher", Integer) #teacher id
    course = Column("course", Integer) #course id
    writer = Column("writer", Integer)  # user id
    content = Column('content', Text)
    views = Column("views", Integer)
    likes = Column("likes", Integer)
    rating = Column("rating", Integer)
    date_written = Column('date_written', DateTime)
    year_taken = Column('year_taken', Integer)



class Course(Base):
    __tablename__ = "courses"

    cid = Column("cid", Integer, primary_key=True)
    name = Column("name", String)
    category = Column("category", String)
    gpa_type = Column("gpa_type", Float)

class Teacher(Base):
    __tablename__ = "teachers"

    tid = Column("tid", Integer, primary_key=True)
    name = Column("name", String)
    email = Column("email", String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)