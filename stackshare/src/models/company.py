from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Companies(Base):

    __tablename__ = 'companies'
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    logo = Column(String, nullable=False)
    site = Column(String)
    token = Column(String)

    def __repr__(self):
        return str(self.__dict__)
