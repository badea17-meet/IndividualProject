from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from database_setup import Base, Dietitian, Client, Appointment

engine = create_engine('sqlite:///lab1.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

if __name__ == ('__main__'):
	newsession = Dietitian(FirstName = "badea")
	session.add(newsession)
	session.commit()