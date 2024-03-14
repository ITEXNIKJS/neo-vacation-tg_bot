import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
import json
import db_con


def start_message(bot: telebot.TeleBot ,message):

    db_con.create_doc_if_not_exist(message.from_user.id)
    btns = []
    btns.append([InlineKeyboardButton(text="Дата отпуска", callback_data="set_date"),InlineKeyboardButton(text="Продолжительность отпуска", callback_data="set_length")])
    btns.append([InlineKeyboardButton(text="Откуда вылет?", callback_data="set_start_point"), InlineKeyboardButton(text="Страны для визита", callback_data="set_countres")])

    btns.append([InlineKeyboardButton(text="Бюджет", callback_data="set_price_range")])
    btns.append([InlineKeyboardButton(text="Посмотреть варианты", callback_data="get_tours")])
    
    keyboard = InlineKeyboardMarkup(btns, row_width=2)
    bot.send_message(chat_id=message.chat.id, text="Привет, я подберу для тебя самые крутые туры, но сначала расскажи о своем отпуске", reply_markup=keyboard)


def listen_date(bot: telebot.TeleBot , message):
    msg = bot.reply_to(message,  text="Отправь мне дату, когда у тебя начинается отпуск \n\nНапример “14 марта 2024”")
    bot.register_next_step_handler(msg, save_data, bot, 'vacation_start_date')


def listen_length(bot: telebot.TeleBot , message):
    msg = bot.reply_to(message,  text="Отправь на сколько дней у тебя отпуск")
    bot.register_next_step_handler(msg, save_data, bot, 'vacation_days')


def listen_countres(bot: telebot.TeleBot , message):
    msg = bot.reply_to(message,  text="Какие страны, города тебе интересны?")
    bot.register_next_step_handler(msg, save_data, bot, 'places_to_visit')


def listen_start_point(bot: telebot.TeleBot , message):
    msg = bot.reply_to(message,  text="Напиши, откуда ты вылетаешь")
    bot.register_next_step_handler(msg, save_data, bot, 'from')


def listen_price(bot: telebot.TeleBot , message):
    msg = bot.reply_to(message,  text="Напиши, какой у тебя бюджет на отпуск")
    bot.register_next_step_handler(msg, save_data, bot, 'max_price_budget')


def save_data(msg, bot: telebot.TeleBot, type:str):
    bot.reply_to(message=msg, text= "Отлично, я запомнил")
    print(msg)
    

    input_data = msg.text
    
 
    db_con.save_in_doc(msg.chat.id, input_data, type)
