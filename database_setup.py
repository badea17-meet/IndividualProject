from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Boolean, DateTime
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
	Height = Column(Float)
	Weight = Column(Float)
	Birthday = Column(DateTime)
	session_id = Column(Integer, ForeignKey('appointment.id'))
	sessions = relationship("Appointment")

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)

class Dietitian(Base):
	__tablename__ = 'ditetitian'
	id = Column(Integer, primary_key=True)
	FirstName = Column(String)
	LastName = Column(String)
	Country = Column(String)
	Email = Column(String)
	ImageURL = Column(String)
	Password = Column(String)
	Gender = Column(String)
	Cellular = Column(String)
	YOE = Column(Float)
	AOE = Column(Float)
	Birthday = Column(DateTime)
	session_id = Column(Integer, ForeignKey('appointment.id'))
	sessions = relationship("Appointment")

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)


class Appointment(Base):
	__tablename__ = 'appointment'
	id = Column(Integer, primary_key=True)
	Client = relationship("Client")
	Time = Column(DateTime)
	Dietitian = relationship("Dietitian")
	Filled = Column(Boolean)








