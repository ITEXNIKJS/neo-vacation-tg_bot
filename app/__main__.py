from main import *
if __name__=="__main__":
      while 1:
        try:
            bot.polling()
        except Exception as e:
            print(e)
            continue