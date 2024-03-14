from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from cfg import MONGOURL
from server_api import get_tours

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
        
def insert_tours(tg_id):
       # visit_target, cur_point, start_date, day_count, max_price
        tours.delete_one({"tg_id":tg_id})
        user_data = db.find_one({'tg_id':tg_id}, {"_id":0})
        for i in range(len(user_data['places_to_visit'])):
            print(user_data['places_to_visit'][i])
            tours_list = get_tours(user_data['places_to_visit'][i]['name'], user_data['from'], user_data["vacation_start_date"], int(user_data["vacation_days"]), int(user_data["max_price_budget"]))
            
            print(tours_list)
            schema = {
                "tg_id": tg_id,
                "tour_data":tours_list
            }
            tours.insert_one(schema)


def get_from_tours_by_tg_id(tg_id):
      tour_data = tours.find_one({"tg_id": tg_id})["tour_data"]
      return tour_data


def get_from_tours_by_tg_id_index(tg_id, index):
      tour_data = tours.find_one({"tg_id": tg_id})["tour_data"][index]
      return tour_data