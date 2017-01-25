from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()

class Client(Base):
	__tablename__ = 'client'
	ID = Column(Integer, primary_key=True)
	FirstName = Column(String)
	LastName = Column(String)
	Country = Column(String)
	Email = Column(String, unique = True)
	ImageURL = Column(String)
	Gender = Column(String)
	Cellular = Column(String)
	Height = Column(Float)
	Weight = Column(Float)
	Birthday = Column(Date)
	password_hash = Column(String(255))
	session_id = Column(Integer, ForeignKey('appointment.id'))
	sessions = relationship("Appointment")

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)

	def set_photo(self, photo):
		self.ImageURL = photo

class Dietitian(Base):
	__tablename__ = 'ditetitian'
	ID = Column(Integer, primary_key=True)
	FirstName = Column(String)
	LastName = Column(String)
	Country = Column(String)
	Email = Column(String)
	ImageURL = Column(String)
	Gender = Column(String)
	Cellular = Column(String)
	YOE = Column(Float)
	AOE = Column(String)
	Birthday = Column(Date)
	password_hash = Column(String(255))
	session_id = Column(Integer, ForeignKey('appointment.id'))
	sessions = relationship("Appointment")

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)

	def set_photo(self, photo):
		self.ImageURL = ImageURL



class Appointment(Base):
	__tablename__ = 'appointment'
	id = Column(Integer, primary_key=True)
	Client = relationship("Client")
	Time = Column(DateTime)
	Dietitian = relationship("Dietitian")
	Filled = Column(Boolean)








