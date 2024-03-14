from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime


uri = "mongodb://localhost:27017/"

client = MongoClient(uri, server_api=ServerApi('1'))
                          


client.admin.command('ping')
db = client["HotLine_Tour"]['users_input']
print("Pinged your deployment. You successfully connected to MongoDB!")



def create_doc_if_not_exist(tg_id):
   
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
        print("Вставка прошла успешно")
    

def save_in_doc(tg_id, input_data, data_type):
        print("123123о")
        db.update_one({"tg_id": tg_id}, {"$set": {f"{data_type}": input_data}})
        print("Вставка прошла успешно")
