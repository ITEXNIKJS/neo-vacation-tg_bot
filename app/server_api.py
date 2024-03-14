import requests
import json
def get_tours(visit_target, cur_point, start_date, day_count, max_price):
    headers = {
        'accept': 'application/json',
    }

    params = {
        'country': visit_target,
        'city': cur_point,
        'start_date': start_date,
        'amount_of_days': day_count,
        'price_min': 0,
        'price_max': max_price,
    }

   
    
    response = requests.get('http://127.0.0.1:8000/api/v1/tour/', params=params, headers=headers)
 
    return json.loads(response.text) 

