#Создание базы данных, если это необходимо

import sqlite3
from sqlalchemy import create_engine, select, MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker
from sqlite3 import Connection as SQLite3Connection
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    author = Column(String)

class Language(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True)
    language = Column(String)

class Expression(Base):
    __tablename__ = "expressions"
    id = Column(Integer, primary_key=True)
    expression = Column(String)

class Expr_Translation(Base):
    __tablename__ = "expr_translation"
    id = Column(Integer, primary_key=True)
    expression = Column(Integer, ForeignKey(Expression.id))
    lang_from = Column(Integer, ForeignKey(Language.id))
    lang_to = Column(Integer, ForeignKey(Language.id))    
    translation = Column(String)

class Title(Base):
    __tablename__ = "titles"
    id = Column(Integer, primary_key=True)
    author = Column(Integer, ForeignKey(Author.id))
    title = Column(String)

class Subtitle(Base):
    __tablename__ = "subtitles"
    id = Column(Integer, primary_key=True)
    title = Column(Integer, ForeignKey(Title.id))
    subtitle = Column(String)
    link = Column(String)

class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    author = Column(Integer, ForeignKey(Author.id))
    title = Column(Integer, ForeignKey(Title.id))
    subtitle = Column(Integer, ForeignKey(Subtitle.id))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login_name = Column(String)
    user_score = Column(Integer)
    user_start = Column(DateTime)
    user_last_add = Column(DateTime)

class Expr_Usage(Base):
    __tablename__ = "expr_usage"
    id = Column(Integer, primary_key=True)
    expression = Column(Integer, ForeignKey(Expression.id))
    translation = Column(Integer, ForeignKey(Expr_Translation.id))
    expr_usage = Column(String)
    usage_source = Column(Integer, ForeignKey(Source.id))
    add_user = Column(Integer, ForeignKey(User.id))
    date_time = Column(DateTime)
    

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

def create_database():
    dbPath = 'ForeignDataFile.db'
    engine = create_engine('sqlite:///%s' % dbPath)
    metadata = MetaData(engine)
    if engine.table_names() == []:
        authors = Table('authors', metadata,
                        Column('id', Integer, primary_key = True),
                        Column('author', String),
                        sqlite_autoincrement=True
                        )
        languages = Table('languages', metadata,
                          Column('id', Integer, primary_key = True),
                          Column('language', String),
                          sqlite_autoincrement=True
                          )
        expressions = Table('expressions', metadata,
                            Column('id', Integer, primary_key= True),
                            Column('expression', String),
                            sqlite_autoincrement=True
                            )
        expr_translation = Table('expr_translation', metadata,
                                 Column('id', Integer, primary_key= True),
                                 Column('lang_from', Integer,
                                        ForeignKey('languages.id')),
                                 Column('lang_to', Integer,
                                        ForeignKey('languages.id')),                                 
                                 Column('expression', Integer,
                                        ForeignKey('expressions.id')),
                                 Column('translation', String),
                                 sqlite_autoincrement=True
                                 )
        titles = Table('titles', metadata,
                       Column('id', Integer, primary_key= True),
                       Column('author', Integer, ForeignKey('authors.id')),
                       Column('title', String),
                       sqlite_autoincrement=True
                       )
        subtitles = Table('subtitles', metadata,
                          Column('id', Integer, primary_key= True),
                          Column('title', Integer,
                                 ForeignKey('titles.id')),
                          Column('subtitle', String),
                          Column('link', String),
                          sqlite_autoincrement=True
                          )
        sources = Table('sources', metadata,
                        Column('id', Integer, primary_key= True),
                        Column('author', Integer, ForeignKey('authors.id')),
                        Column('title', Integer, ForeignKey('titles.id')),
                        Column('subtitle', Integer, ForeignKey('subtitles.id')),
                        sqlite_autoincrement=True
                        )
        users = Table('users', metadata,
                      Column('id', Integer, primary_key= True),
                      Column('login_name', String),
                      Column('user_score', Integer),
                      Column('user_start', DateTime),
                      Column('user_last_add', DateTime),
                      sqlite_autoincrement=True
                      )
        expr_usage = Table('expr_usage', metadata,
                           Column('id', Integer, primary_key= True),
                           Column('expression', Integer,
                                  ForeignKey('expressions.id')),
                           Column('translation', Integer,
                                  ForeignKey('expr_translation.id')),
                           Column('expr_usage', String),
                           Column('usage_source', Integer,
                                  ForeignKey('sources.id')),
                           Column('add_user', Integer,
                                  ForeignKey('users.id')),
                           Column('date_time', DateTime),
                           sqlite_autoincrement=True
                           )
        Session = sessionmaker(bind = engine)
        session = Session()
        metadata.create_all(engine)
        session.commit()
        print(engine.table_names())
        lang1 = languages.insert().values(language = 'English')
        lang2 = languages.insert().values(language = 'Русский')
        date_time = datetime.datetime.now()
        user = users.insert().values(login_name = "admin", user_score = 0,
                                     user_start = date_time,
                                     user_last_add = date_time)
        session.execute(lang1)
        session.execute(lang2)
        session.execute(user)
        session.commit()
        result = session.execute(select([languages]))
        for row in result:
            print(row)
        result = session.execute(select([users]))
        for row in result:
            print(row)

def connect_to_base():
    dbPath = 'ForeignDataFile.db'
    engine = create_engine('sqlite:///%s' % dbPath)
    Session = sessionmaker(bind = engine)
    session = Session()
    return session

def connect_to_new_base(file_name):
    dbPath = file_name
    engine = create_engine('sqlite:///%s' % dbPath)
    Session = sessionmaker(bind = engine)
    session = Session()
    return session

if __name__ == '__main__':
    create_database()
    
