import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
import json
import db_con
import validations

'''Функции ответа на нажатые кнопки и сохранение в MongoDB'''



def start_message(bot: telebot.TeleBot ,message):

    db_con.create_doc_if_not_exist(message.from_user.id)
    btns = []
    btns.append([InlineKeyboardButton(text="🤿 Дата отпуска", callback_data="set_date"),InlineKeyboardButton(text="⌛ Продолжительность отпуска", callback_data="set_length")])
    btns.append([InlineKeyboardButton(text="✈ Откуда вылет?", callback_data="set_start_point"), InlineKeyboardButton(text="🌏 Страны для визита", callback_data="set_countres")])

    btns.append([InlineKeyboardButton(text="💰 Бюджет", callback_data="set_price_range")])
    btns.append([InlineKeyboardButton(text="🔎 Посмотреть варианты", callback_data="get_tours")])
    
    keyboard = InlineKeyboardMarkup(btns, row_width=2)
    bot.send_message(chat_id=message.chat.id, text="🖐 Привет, я подберу для тебя самые крутые туры, но сначала расскажи о своем отпуске", reply_markup=keyboard)


def listen_date(bot: telebot.TeleBot , message):
    msg = bot.reply_to(message,  text="Отправь мне 📅 дату, когда у тебя начинается отпуск \n\nНапример “14.03.2024”")
    bot.register_next_step_handler(msg, save_data, bot, 'vacation_start_date')


def listen_length(bot: telebot.TeleBot , message):
    msg = bot.reply_to(message,  text="Отправь на сколько ☀ дней у тебя отпуск (макс 19 день из-за ограничений провайдера информации)")
    bot.register_next_step_handler(msg, save_data, bot, 'vacation_days')


def listen_countres(bot: telebot.TeleBot , message):
    msg = bot.reply_to(message,  text="Какие 🏴‍☠️страны тебе интересны?")    
    bot.register_next_step_handler(msg, save_data_countries, bot, 'places_to_visit')



def listen_start_point(bot: telebot.TeleBot , message):
    msg = bot.reply_to(message,  text="Напиши, 📍 откуда ты вылетаешь")
    bot.register_next_step_handler(msg, save_data_countries, bot, 'from')


def listen_price(bot: telebot.TeleBot , message):
    msg = bot.reply_to(message,  text="Напиши, какой у тебя 💸 бюджет в ₽ на отпуск")
    bot.register_next_step_handler(msg, save_data, bot, 'max_price_budget')


def save_data(msg, bot: telebot.TeleBot, type:str):
    if type =="vacation_start_date" and not validations.validate_date(msg.text):
        bot.send_message(msg.chat.id, text=f"😢 Дата {msg.text} не того формата либо это уже прошедший день. Введите День, месяц и год через точку: 15.03.2024")
        return
    if type =="vacation_days" and not validations.validate_integer(msg.text):
        bot.send_message(msg.chat.id, text=f"😢 Введите целое число не более 19 (из-за ограничений Провайдера информации)")
        return
    if type =="from" :
        entered = msg.text.split(sep=', ')
        input_data=[]
        for e in entered:
            js = db_con.find_by_name(e)
            if js =="404":
                bot.send_message(msg.chat.id, text=f"😢 Такого города еще нет в наших данных")
                return
            else:
                input_data.append(js)

    if type =="max_price_budget" and not validations.validate_price(msg.text):
        bot.send_message(msg.chat.id, text=f"😢 Для работы нужно целое число без знаков, не ломайте меня(")
        return

    bot.reply_to(message=msg, text= "👌 Отлично, я запомнил")
    print(msg)
    input_data = msg.text
    db_con.save_in_doc(msg.chat.id, input_data, type)
    start_message(bot, msg)


def save_data_countries(msg, bot: telebot.TeleBot, type:str):

    entered = msg.text.split(sep=', ')
    input_data=[]
    for e in entered:
        js = db_con.find_by_name(e)
        if js =="404":
             if type =='from':
                bot.send_message(msg.chat.id, text=f"😢 Из {e} еще не возим")
             else:
                bot.send_message(msg.chat.id, text=f"😢 В {e} еще не возим")
             return
        elif len(js)==3 and type=="places_to_visit":
            bot.send_message(msg.chat.id, text=f"😢 Укажи тут страну")
            return
        elif len(js)==5 and type=="from":
            bot.send_message(msg.chat.id, text=f"😢 Укажи тут свой город России")
            return

        if type=="from":   
            input_data= js['name']
            break
        else:
            input_data.append(js)
   
    
    db_con.save_in_doc(msg.chat.id, input_data, type)
    bot.reply_to(message=msg, text= "👌 Отлично, я запомнил")
    start_message(bot, msg)
        
 
   