# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Stacks(Base):

    __tablename__ = 'stacks'

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    contents = Column(String)
    description = Column(String)
    star_count = Column(String)
    votes_count = Column(String)
    fans_count = Column(String)
    stacks_count = Column(String)
    integrations_count = Column(String)
    companies = Column(String)
    name = Column(String)

    def __repr__(self):
        return str(self.__dict__)
