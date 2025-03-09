from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.orm import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)
#Database setup
engine = create_engine("sqlite:///theater_work.db") #connect to the database
Session = sessionmaker(bind=engine) #bind the engine to the session
session = Session() #create the session




class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)
    #One to many relationship
    auditions = relationship("Audition", backref=backref("role", cascade="all, delete-orphan"))

@property
def actors(self):
        return [audition.actor for audition in self.auditions]

@property
def locations(self):
        return [audition.location for audition in self.auditions]

def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[0] if hired_auditions else "No actor has been hired for this role"

def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[1] if len(hired_auditions) > 1 else "No actor has been hired for understudy for this role"



class Audition(Base):
    __tablename__ = "auditions"
    id = Column(Integer, primary_key=True)
    actor = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(Integer, nullable=False)
    hired = Column(Boolean, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))

    def call_back(self):# change hired to true
        self.hired = True
        session.commit()


