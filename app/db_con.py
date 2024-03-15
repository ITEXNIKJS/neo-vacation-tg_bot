from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from cfg import MONGOURL
from server_api import get_tours
import pandas as pd
import alka

'''Подключение к MongoDB и функции работы с документом бота'''

uri = MONGOURL

client = MongoClient(uri, server_api=ServerApi('1'))
                          


client.admin.command('ping')
db = client["HotLine_Tour"]['users_input']
cities =client["HotLine_Tour"]['cities'] 
countries =client["HotLine_Tour"]['countries'] 
tours = client["HotLine_Tour"]['tours']

print("Pinged your deployment. You successfully connected to MongoDB!")



def create_doc_if_not_exist(tg_id):
    #вызывается при /start
        schema = {
            "tg_id": tg_id,
            "vacation_start_date": "",
            "vacation_days": 0,
            "places_to_visit": [],
            "from": "",
            "max_price_budget": 0,
            "min_price_budget": 0
        
        }
        db.update_one({"tg_id": tg_id}, {"$setOnInsert": schema}, upsert=True)
        print("create_doc_if_not_exist Вставка прошла успешно")
    

def save_in_doc(tg_id, input_data, data_type):
        #после каждого ответа пользователя
        db.update_one({"tg_id": tg_id}, {"$set": {f"{data_type}": input_data}})
        print("save_in_doc Вставка прошла успешно")


def get_body_by_tg_id(tg_id):
        #Тело запроса к API
        return db.find_one({"tg_id":tg_id}, {"_id": 0, "tg_id": 0})
        #{'from': '', 'max_price_budget': 0, 'min_price_budget': 0, 'places_to_visit': [], 'vacation_days': '122', 'vacation_start_date': '123\\'}
        
def find_by_name(name):
      
        pipeline = [
        {"$unwind": "$cities"},  # Развернуть массив городов
        {"$match": {"cities.name": {"$regex": f"{name}", "$options": "i"}}}  # Найти город по имени
            ]
        citys = cities.aggregate(pipeline)

        pipeline = [
        {"$unwind": "$countries"},  
        {"$match": {"countries.name": {"$regex": f"{name}", "$options": "i"}}} ]
        countrys = countries.aggregate(pipeline)
        if citys:
            for city in citys:
                 if city!=None:
                      return city['cities']
        if countrys:
              for country in countrys:
                if country!=None:
                      return country["countries"]
        return "404"

def clenup_tours(tg_id):
    tours = client["HotLine_Tour"]['tours']
    # Получение всех туров
    tours_list = list(tours.find({"tg_id": tg_id}, {"_id": 0}))

    # Фильтрация и сортировка туров
    filtered_tours_list = []
    for tour in tours_list:
        # Фильтрация туров по категории
        category = tour['tour_data'][0]['Категория']
        if category not in filtered_tours_list:
            filtered_tours_list.append(category)

        # Фильтрация и сортировка туров в каждой категории
        category_tours = [tour for tour in tours_list if tour['tour_data'][0]['Категория'] == category]
        category_tours.sort(key=lambda x: x['tour_data'][0]['Цена'], reverse=True)
        filtered_tours_list.append(category_tours[:4])

    # Вывод результатов
    for category, tours in zip(filtered_tours_list[::2], filtered_tours_list[1::2]):
        print(f"Категория: {category}")
        for tour in tours:
            print(tour)

def insert_tours(tg_id):
       # visit_target, cur_point, start_date, day_count, max_price
        tours.delete_one({"tg_id":tg_id})
        user_data = db.find_one({'tg_id':tg_id}, {"_id":0})
        for i in range(len(user_data['places_to_visit'])):
            print(user_data['places_to_visit'][i])
            
            tours_list = get_tours(alka.select_user_ids_by_tg_id(tg_id) ,user_data['places_to_visit'][i]['name'], user_data['from'], user_data["vacation_start_date"], int(user_data["vacation_days"]), int(user_data["max_price_budget"]))
            if i==0:
                print(tours_list)
                schema = {
                    "tg_id": tg_id,
                    "tour_data":tours_list
                }
                tours.insert_one(schema)
            else:
                  for q in tours_list:
                     tours.update_one({"tg_id": tg_id}, {"$push": {"tour_data": q}},upsert=True)


def get_from_tours_by_tg_id(tg_id):

      return get_best_tours_by_category(tg_id)


def get_from_tours_by_tg_id_index(tg_id, index):
     

      return get_best_tours_by_category(tg_id)[index]

import pandas as pd
from pymongo import MongoClient

def get_best_tours_by_category(tg_id):
    # Подключение к MongoDB

    # Получение данных из MongoDB
    data = list(tours.find_one({"tg_id": tg_id})["tour_data"])

    # Создаем словарь для хранения лучших туров по категориям
    best_tours = {}
    if len(data)==1: return "Туры по указанным параметрам не найдены"
    # Итерируем по данным и выбираем лучший тур для каждой категории
    for tour in data:
        category = tour['Категория']
        price = tour['Цена']
        if category not in best_tours or price < best_tours[category]['Цена']:
            best_tours[category] = tour

    return list(best_tours.values())


def check_input(tg_id):
    schema = {
            "tg_id": tg_id,
            "vacation_start_date": "",
            "vacation_days": 0,
            "places_to_visit": [],
            "from": "",
            "max_price_budget": 0,
            "min_price_budget": 0
        
        }
    
    u_input = dict(db.find_one({ "tg_id": tg_id}))
    matches = []
    keys=["vacation_start_date","vacation_days", "places_to_visit", "from", "max_price_budget"]  
    
    for i in keys:
        if u_input[i] == schema[i]:
            matches.append(i)
    return matches

print(check_input(406895370))