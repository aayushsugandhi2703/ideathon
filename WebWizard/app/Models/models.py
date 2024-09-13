from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Engine = create_engine('''sqlite:///database.db''')

Base = declarative_base()

class User(UserMixin,Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    contact = relationship('Contact', back_populates='user',cascade='all, delete, delete-orphan')

@property
def is_active(self):
    return True

@property
def is_anonymous(self):
    return False

@property
def is_authenticated(self):
    return True

class Contact(UserMixin, Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    amount = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='contact')

session = sessionmaker(bind=Engine)

Session = session()

Base.metadata.create_all(Engine)