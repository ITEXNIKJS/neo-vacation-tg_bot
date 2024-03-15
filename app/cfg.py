
from dotenv import dotenv_values

# Загрузка переменных из файла .env в виде словаря
env_vars = dotenv_values()

TOKEN = env_vars.get('TOKEN')
MONGOURL=env_vars.get('MONGOURL')
ENGINE_URL=env_vars.get('ENGINE_URL')
SERVER_ENDP=env_vars.get('SERVER_ENDP')