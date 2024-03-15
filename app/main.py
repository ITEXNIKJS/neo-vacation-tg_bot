import telebot
from cfg import TOKEN
from datetime import datetime
import functions
import logging
import tour_functions
'''
Обработчики всех возможных кнопок и вводов из чата ТГ
'''

bot = telebot.TeleBot(TOKEN)
start_time = datetime.now()
print("Start time is", start_time)
current_month = datetime.now().month

# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)

@bot.message_handler(commands=["start"])
def start_answer(message):
    functions.start_message(bot, message)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'set_date':
        functions.listen_date(bot, call.message)
        
    elif call.data == 'set_length':
        functions.listen_length(bot, call.message)
    
    elif call.data == 'set_countres':
        functions.listen_countres(bot, call.message)
        
    elif call.data == 'set_start_point':
        functions.listen_start_point(bot, call.message)
    
    elif call.data == 'set_price_range':
        functions.listen_price(bot, call.message)

    elif call.data == 'get_tours':
        tour_functions.routs_start_message(bot, call)
        
    elif call.data == 'send_query':
        bot.delete_message(call.message.chat.id, call.message.id)
        tour_functions.answer_on_query(bot, call)
    
    elif "previous_page" in call.data:
        tour_functions.change_page(bot, call, -1)

    elif "next_page" in call.data:
        tour_functions.change_page(bot, call, 1)

    elif call.data == 'edit':
        bot.delete_message(call.message.chat.id, call.message.id)