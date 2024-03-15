from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'

    id = Column(String, primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    login = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    tg_id = Column(Integer, unique=True)
    tg_username = Column(String, unique=True)


   


engine = create_engine('cockroachdb://neohack:CectGfJj0TEhKlvUmN_0hQ@neo-hack-vacantion-14064.8nj.gcp-europe-west1.cockroachlabs.cloud:26257/neohack-vacation-website', 
                       connect_args={'sslmode': "allow"}, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

def check_user(tg_id):
   
    user = session.query(User).filter_by(tg_id=tg_id).first()
    return user is not None

def select_user_ids_by_tg_id(tg_id):

    user_ids = session.query(User.id).filter(User.tg_id == tg_id).first()
    return user_ids[0]

print(select_user_ids_by_tg_id(637382945))