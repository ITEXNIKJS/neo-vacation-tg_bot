import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
import db_con
import server_api
from datetime import datetime
import alka
def routs_start_message(bot: telebot.TeleBot ,call):

    #проверка на заполненность
    unfilded = db_con.check_input(call.from_user.id)
    if unfilded!=[]:
        alert_message ="Вы не заполнили "
        for i in unfilded:
            alert_message+= i+"\n"
        bot.answer_callback_query(call.id, text= alert_message, show_alert=True)
        return


    query_info = db_con.get_body_by_tg_id(call.from_user.id)
    countries = ""
    for i in query_info["places_to_visit"]:
        countries+=i['name']+", "
    countries =countries[:-2]
    answer = f'''Проверь, все ли верно?\n
    Ты собираешься в отпуск {query_info['vacation_start_date']} на {query_info["vacation_days"]} дней
    Вылет из {query_info["from"]}, а направляешься в {countries}
    Бюджет до {query_info["max_price_budget"]} ₽ 
    '''

    btns = []
    btns.append([InlineKeyboardButton(text="Все Верно", callback_data="send_query"),InlineKeyboardButton(text="Внести поправки", callback_data="edit")])
    keyboard = InlineKeyboardMarkup(btns, row_width=2)
    bot.send_message(chat_id=call.message.chat.id, text=answer, reply_markup=keyboard)


def answer_on_query(bot: telebot.TeleBot ,call):
    
    
    bot.send_message(call.message.chat.id, text= "⚙Собираем Информацию")
    db_con.insert_tours(call.from_user.id)
    render_list_range = len(db_con.get_from_tours_by_tg_id(call.from_user.id))
    if render_list_range==0:
        bot.send_message(chat_id=call.message.chat.id, text="Мы ничего не нашли, попробуйте подвинуть дату")
        return
    btns=[]
   
    cur_page = 0
    tour = db_con.get_from_tours_by_tg_id_index(call.from_user.id, cur_page)
    # date_object = datetime.strptime(tour["Дата заезда"], '%Y-%m-%dT%H:%M:%S')
    # formatted_date = date_object.strftime("%Y.%m.%d")
    answer = f'''Найдено {render_list_range} туров\n\nТур №{cur_page+1}\n
🏆   Вот {tour['Категория']}\n
📅   Дата заезда: {tour["Дата заезда"]} 
🕕   Длительность в ночах: {tour["Длительность в ночах"]} 
🌏   Регион проживания: {tour["Регион проживания"]} 
🏨   Отель:  {tour["Отель"]} 
🍖   Пансион:  {tour["Пансион"]} 
🛌   Тип номера: {tour["Тип номера"]} 
💵   Цена:  {tour["Цена"]}₽'''
    cur_page
    if(cur_page>0 and cur_page!=render_list_range-1 ):
      btns.append([InlineKeyboardButton(text="<<", callback_data=f"previous_page_{cur_page}_{render_list_range}") ,InlineKeyboardButton(text="🛒 Купить тур", callback_data=f"buy_{cur_page}"),InlineKeyboardButton(text="📱Перейти на сайт", url=tour["Доступные места в отеле"]),InlineKeyboardButton(text=">>", callback_data=f"next_page_{cur_page}_{render_list_range}")]) 
    elif cur_page==render_list_range-1:
        btns.append([InlineKeyboardButton(text="<<", callback_data=f"previous_page_{cur_page}_{render_list_range}") ,InlineKeyboardButton(text="🛒 Купить тур", callback_data=f"buy_{cur_page}"),InlineKeyboardButton(text="📱Перейти на сайт", url=tour["Доступные места в отеле"])]) 
    elif cur_page <=0:
        btns.append([InlineKeyboardButton(text="🛒 Купить тур", callback_data=f"buy_{cur_page}"), InlineKeyboardButton(text="📱Перейти на сайт", url=tour["Доступные места в отеле"]),InlineKeyboardButton(text=">>", callback_data=f"next_page_{cur_page}_{render_list_range}")]) 

    keyboard = InlineKeyboardMarkup(btns, row_width=3)
    bot.send_message(chat_id=call.message.chat.id, text=answer, reply_markup=keyboard, parse_mode="HTML")

def change_page(bot: telebot.TeleBot ,call , step):
    cur_page = int(call.data.split(sep="_")[2])+step

    len = int(call.data.split(sep="_")[3])

  
    btns=[]
   
    tour = db_con.get_from_tours_by_tg_id_index(call.from_user.id, cur_page)
    
    # date_object = datetime.strptime(tour["Дата заезда"], '%Y-%m-%dT%H:%M:%S')
    # formatted_date = date_object.strftime("%Y.%m.%d")
    answer = f'''Найдено {len} туров\n\nТур №{cur_page+1}\n
🏆   Вот {tour['Категория']}\n
📅   Дата заезда: {tour["Дата заезда"]} 
🕕   Длительность в ночах: {tour["Длительность в ночах"]} 
🌏   Регион проживания: {tour["Регион проживания"]} 
🏨   Отель:  {tour["Отель"]} 
🍖   Пансион:  {tour["Пансион"]} 
🛌   Тип номера: {tour["Тип номера"]} 
💵   Цена:  {tour["Цена"]}₽'''
    
    if(cur_page>0 and cur_page!=len-1 ):
      btns.append([InlineKeyboardButton(text="<<", callback_data=f"previous_page_{cur_page}_{len}") ,InlineKeyboardButton(text="🛒 Купить тур", callback_data=f"buy_{cur_page}"),InlineKeyboardButton(text="📱Перейти на сайт", url=tour["Доступные места в отеле"]),InlineKeyboardButton(text=">>", callback_data=f"next_page_{cur_page}_{len}")]) 
    elif cur_page==len-1:
        btns.append([InlineKeyboardButton(text="<<", callback_data=f"previous_page_{cur_page}_{len}") ,InlineKeyboardButton(text="🛒 Купить тур", callback_data=f"buy_{cur_page}"),InlineKeyboardButton(text="📱Перейти на сайт", url=tour["Доступные места в отеле"])]) 
    elif cur_page <=0:
        btns.append([InlineKeyboardButton(text="🛒 Купить тур", callback_data=f"buy_{cur_page}"), InlineKeyboardButton(text="📱Перейти на сайт", url=tour["Доступные места в отеле"]),InlineKeyboardButton(text=">>", callback_data=f"next_page_{cur_page}_{len}")]) 

    keyboard = InlineKeyboardMarkup(btns, row_width=4)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id ,text=answer,  reply_markup=keyboard, parse_mode="HTML")


def buy_req(bot: telebot.TeleBot ,call):
    cur_page = int(call.data.split(sep="_")[1])
    doc = db_con.get_from_tours_by_tg_id_index(call.from_user.id, cur_page)
    alka.insert_order(alka.select_user_ids_by_tg_id(call.from_user.id), doc)
    bot.send_message(chat_id=call.message.chat.id, text="Отправил запрос на покупку")