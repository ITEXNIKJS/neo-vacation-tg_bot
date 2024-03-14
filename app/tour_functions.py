import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
import db_con

def routs_start_message(bot: telebot.TeleBot ,call):
    query_info = db_con.get_body_by_tg_id(call.from_user.id)
    countries = ""
    for i in query_info["places_to_visit"]:
        countries+=i['name']+", "
    countries =countries[:-2]
    answer = f'''Проверь, все ли верно?\n
    Ты собираешься в отпуск {query_info['vacation_start_date']} на {query_info["vacation_start_date"]} дней
    Вылет из {query_info["from"]}, а направляешься в {countries}
    Бюджет до {query_info["max_price_budget"]} ₽ 
    '''

    btns = []
    btns.append([InlineKeyboardButton(text="Все Верно", callback_data="send_query"),InlineKeyboardButton(text="Внести поправки", callback_data="edit")])
    keyboard = InlineKeyboardMarkup(btns, row_width=2)
    bot.send_message(chat_id=call.message.chat.id, text=answer, reply_markup=keyboard)

