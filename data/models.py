from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, Boolean, create_engine, ForeignKey
from sqlalchemy_utils import EmailType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
# SQLAlchemy setup
DATABASE_URL = "postgresql://postgres:qwerty123@localhost:5432/webtronics"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(EmailType, unique=True, index=True)
    password = Column(String)

    rates = relationship("Rate", backref="users")


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    password_repeat: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    email: str


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)

    rates = relationship("Rate", backref="post")


class PostCreateSchema(BaseModel):
    content: str


class PostDeleteSchema(BaseModel):
    id: int


class PostEditSchema(BaseModel):
    id: int
    content: str


class PostResponseSchema(BaseModel):
    id: int
    author_id: int
    content: str


class Rate(Base):
    __tablename__ = 'rates'
    id = Column(Integer, primary_key=True, index=True)
    like = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))


class RatePostSchema(BaseModel):
    like: bool
