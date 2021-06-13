from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.functions import user
from db import User, Review, Course, Teacher, Session
from datetime import datetime
import random
import time


def get_courses():
    session = Session()
    courses = session.query(Review).all()
    session.close()
    return courses


def get_teachers():
    session = Session()
    teachers = session.query(Teacher).all()
    session.close()
    return teachers


def next_id(db):
    session = Session()
    if db == "user":
        first = session.query(func.max(User.uid)).first()[0]
    elif db == "review":
        first = session.query(func.max(Review.rid)).first()[0]
    session.close()

    if first != None:
        return first + 1
    else:
        return 0


class Users:
    def __init__(self, uid, username, password, email):
        self.attributes = ["uid", 'username', 'password', 'email']
        self.uid = uid
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def from_new(cls, username, password, email):
        session = Session()
        user = User()
        uid = next_id("user")
        user.uid = uid
        user.username = username
        user.password = password
        user.email = email
        session.add(user)
        session.commit()
        session.close()

        return cls(uid, username, password, email)

    @classmethod
    def from_db(cls, uid):
        session = Session()
        user = session.query(User).filter_by(uid=uid).first()
        username = user.username
        password = user.password
        email = user.email
        session.close()

        return cls(uid, username, password,  email)

    # attribute is string of the attribute variable to be updated
    def update_attribute(self, attribute, new_value):
        if attribute not in self.attributes:
            raise Exception('attibute does not exist')

        session = Session()
        user = session.query(User).filter_by(uid=self.uid).first()
        exec(f"user.{attribute} = new_value")
        exec(f"self.{attribute} = new_value")
        session.add(user)
        session.commit()
        session.close()

    def make_review(self, publicity, teacher, course, content, rating, date_written, year_taken):
        Reviews.from_new(publicity, teacher, course, self.uid,
                         content, 0, 0, rating, date_written, year_taken)


class Reviews:
    def __init__(self, rid, publicity, teacher, course, writer, content, views, likes, rating, date_written, year_taken):
        self.attibutes = ['rid', 'publicity', 'teacher', 'course', 'writer',
                          'content', 'views', 'likes', 'rating', 'date_written', 'year_taken']
        self.rid = rid
        self.publicity = publicity
        self.teacher = teacher
        self.course = course
        self.writer = writer
        self.content = content
        self.views = views
        self.likes = likes
        self.rating = rating
        self.date_written = date_written
        self.year_taken = year_taken

    @classmethod
    def from_new(cls, publicity, teacher, course, writer, content, views, likes, rating, date_written, year_taken):
        session = Session()
        review = Review()
        rid = next_id("review")

        review.rid = rid
        review.publicity = publicity
        review.teacher = teacher
        review.course = course
        review.writer = writer
        review.content = content
        review.views = views
        review.likes = likes
        review.rating = rating
        review.date_written = date_written
        review.year_taken = year_taken
        session.add(review)
        session.commit()
        session.close()

        return cls(rid, publicity, teacher, course, writer, content, views, likes, rating, date_written, year_taken)

    @classmethod
    def from_db(cls, rid):
        session = Session()
        review = session.query(Review).filter_by(rid=rid).first()
        rid = review.rid
        publicity = review.publicity
        teacher = review.teacher
        course = review.course
        writer = review.writer
        content = review.content
        views = review.views
        likes = review.likes
        rating = review.rating
        date_written = review.date_written
        year_taken = review.year_taken
        session.close()
        return cls(rid, publicity, teacher, course, writer, content, views, likes, rating, date_written, year_taken)

    # attribute is (lowercase) string of the attribute variable to be updated
    def update_attribute(self, attribute, new_value):
        if attribute not in self.attributes:
            raise Exception('attibute does not exist')

        session = Session()
        review = session.query(Review).filter_by(rid=self.rid).first()
        exec(f"review.{attribute} = new_value")
        exec(f"self.{attribute} = new_value")
        session.add(review)
        session.commit()
        session.close()


# tester code

# a = Users.from_new('asdf', 'asdfasdf', 'exemail')
# b = Users.from_new('2', '23', 'exemail123')

# a = Users.from_db(0)
# print(a.email)

# b = Users.from_db(0)
# print(b.email)

# b.update_attribute('email', 'asdfasdasdff@gmail.com')

# b.make_review(False,0,0, 'hello thisasdf is my review ahahahaha',5,datetime.now(),2019)
