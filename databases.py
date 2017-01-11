from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Client(Base):
	__tablename__ = 'client'
	id = Column(Integer, primary_key=True)
	FirstName = Column(String)
	LastName = Column(String)
	Country = Column(String)
	Email = Column(String)
	ImageURL = Column(String)
	Password = Column(String)
	Gender = Column(String)
	Cellular = Column(String)
	Height = Colimn(Float)
	Weight = Column(Float)
	Birthday = Column(DateTime)

class Dietitian(Base):
	__tablename__ = 'declarativeietitian'
	id = Column(Integer, primary_key=True)
	FirstName = Column(String)
	LastName = Column(String)
	Country = Column(String)
	Email = Column(String)
	ImageURL = Column(String)
	Password = Column(String)
	Gender = Column(String)
	Cellular = Column(String)
	YOE = Colimn(Float)
	AOE = Column(Float)
	Birthday = Column(DateTime)

class DietitianSessions(Base):
	__tablename__ = 'dietitiansessions'
	SessionID = Column(Integer, primary_key=True)
	Client = Column(String)
	Time = Column(DateTime)
	Dietitian = Column(String)

class ClientSessions(Base):
	__tablename__ = 'clientsessions'
	SessionID = Column(Integer, primary_key=True)
	Client = Column(String)
	Time = Column(DateTime)
	Dietitian = Column(String)
	