from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Companies(Base):

    __tablename__ = 'companies'

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    company_name = Column(String, nullable=False)
    logo = Column(String, nullable=False)

    def __repr__(self):
        return str(self.__dict__)
