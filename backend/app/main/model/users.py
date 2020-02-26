from sqlalchemy import Integer, String, Column, Table

from database import metadata

user = Table('users', metadata,
             Column('id', Integer, primary_key=True),
             Column('username', String(50), unique=True),
             Column('repositories', String)
             )
