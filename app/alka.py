from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import os
from cfg import ENGINE_URL

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'

    id = Column(String, primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    login = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    tg_id = Column(Integer, unique=True)
    tg_username = Column(String, unique=True)
    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = 'Order'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    dateIn = Column(DateTime)
    duration = Column(Integer)
    country = Column(String)
    hotel = Column(String)
    pansion = Column(String)
    room_type = Column(String)
    price = Column(Integer)
    available_places = Column(String)
    price_with_loss = Column(Integer)
    category = Column(String)
    boarding = Column(String)
    userId = Column(String, ForeignKey('User.id'))
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="orders")


engine = create_engine(ENGINE_URL, 
                       connect_args={'sslmode': "allow"}, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

def check_user(tg_id):
   
    user = session.query(User).filter_by(tg_id=tg_id).first()
    return user is not None

def select_user_ids_by_tg_id(tg_id):

    user_ids = session.query(User.id).filter(User.tg_id == tg_id).first()
    return user_ids[0]

def insert_order(user_id, data):
    new_order = Order(
        userId=user_id,
        dateIn=datetime.strptime(data.get("Дата заезда"), "%d.%m.%Y"),
        duration=data.get("Длительность в ночах"),
        country=data.get("Регион проживания"),
        hotel=data.get("Отель"),
        pansion=data.get("Пансион"),
        room_type=data.get("Тип номера"),
        price=data.get("Цена"),
        available_places=data.get("Доступные места в отеле"),
        price_with_loss=data.get("Цена с убытком"),
        category=data.get("Категория"),
        boarding=data.get("Город вылета")
    )
    session.add(new_order)
    session.commit()


print(select_user_ids_by_tg_id(637382945))