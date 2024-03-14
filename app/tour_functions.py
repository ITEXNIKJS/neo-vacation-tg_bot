import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
import db_con
import server_api

def routs_start_message(bot: telebot.TeleBot ,call):
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
    bot.send_message(call.message.chat.id, text= "Собираем Информацию")
    db_con.insert_tours(call.from_user.id)
    render_list_range = len(db_con.get_from_tours_by_tg_id(call.from_user.id))
    if render_list_range==0:
        bot.send_message(chat_id=call.message.chat.id, text="Мы ничего не нашли, попробуйте подвинуть дату")
        return
    btns=[]
    btns.append([InlineKeyboardButton(text="<<", callback_data=f"previous_page_0_{render_list_range}"),InlineKeyboardButton(text=">>", callback_data=f"next_page_0_{render_list_range}")])
    keyboard = InlineKeyboardMarkup(btns, row_width=2)
    cur_page = 0
    tour = db_con.get_from_tours_by_tg_id_index(call.from_user.id, cur_page)
    answer = f'''Найдено {render_list_range} туров\n\nТур №{cur_page+1}\n
    Дата заезда: {tour["Дата заезда"]}
    Длительность в ночах: {tour["Длительность в ночах"]}
    Регион проживания: {tour["Регион проживания"]}
    Отель: {tour["Отель"]}
    Пансион: {tour["Пансион"]}
    Тип номера: {tour["Тип номера"]}
    Цена: {tour["Цена"]}
    Доступные места в отеле: {tour["Доступные места в отеле"]}'''
    bot.send_message(chat_id=call.message.chat.id, text=answer, reply_markup=keyboard)

def change_page(bot: telebot.TeleBot ,call , step):
    cur_page = int(call.data.split(sep="_")[2])+step

    len = int(call.data.split(sep="_")[3])

  
    btns=[]
    btns.append([InlineKeyboardButton(text="<<", callback_data=f"previous_page_{cur_page}_{len}"),InlineKeyboardButton(text=">>", callback_data=f"next_page_{cur_page}_{len}")])
    keyboard = InlineKeyboardMarkup(btns, row_width=2)
    tour = db_con.get_from_tours_by_tg_id_index(call.from_user.id, cur_page)
    answer = f'''Найдено {len} туров\n\nТур №{cur_page+1}\n
    Дата заезда: {tour["Дата заезда"]}
    Длительность в ночах: {tour["Длительность в ночах"]}
    Регион проживания: {tour["Регион проживания"]}
    Отель: {tour["Отель"]}
    Пансион: {tour["Пансион"]}
    Тип номера: {tour["Тип номера"]}
    Цена: {tour["Цена"]}
    Доступные места в отеле: {tour["Доступные места в отеле"]}'''

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id ,text=answer,  reply_markup=keyboard)