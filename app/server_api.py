import requests
import json
from dotenv import dotenv_values
env_vars = dotenv_values()

def get_tours(tg_id,visit_target, cur_point, start_date, day_count, max_price):
    headers = {
        'accept': 'application/json',
    }

    params = {
        "user_id":str(tg_id),
        'country': visit_target,
        'city': cur_point,
        'start_date': start_date,
        'amount_of_days': day_count,
        'price_min': 0,
        'price_max': max_price,
    }

   
    
    response = requests.get(env_vars.get('SERVER_ENDP'), params=params, headers=headers)
 
    return json.loads(response.text) 

