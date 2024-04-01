import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message             # ловим все обновления этого типа 
from aiogram.filters.command import Command   # обрабатываем команды /start, /help и другие

def translit(message):
    table = {
        'А': 'A', 'Б': 'B',
        'В': 'V', 'Г': 'G',
        'Д': 'D', 'Е': 'E',
        'Ё': 'E', 'Ж': 'ZH',
        'З': 'Z', 'И': 'I',
        'Й': 'I', 'К': 'K',
        'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O',
        'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T',
        'У': 'U', 'Ф': 'F',
        'Х': 'KH', 'Ц': 'TS',
        'Ч': 'CH', 'Ш': 'SH',
        'Щ': 'SHCH', 'Ы': 'Y',
        'Ъ': 'IE', 'Э': 'E',
        'Ю': 'IU', 'Я': 'IA',
        ' ': ' ', 'Ь': "'"
    }
    name = message.upper()
    latin_name = ''
    for i in name:
        if (i.isalpha() and 'А' <= i <= 'Я') or (i == ' '):
            latin_name += table[i]
        else:
            return 'Вводите только кириллические символы и пробел'    
    return latin_name.title()   

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)                       # Создаем объект бота
dp = Dispatcher()                             # Создаем объект диспетчера. Все хэндлеры(обработчики) должны быть подключены к диспетчеру
logging.basicConfig(level=logging.INFO, filename='botlog.txt')

@dp.message(Command(commands=['start']))
async def proccess_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f'Привет, {user_name}!'
    logging.info(f'{user_name} {user_id} запустил бота')
    await bot.send_message(chat_id=user_id, text=text)
    
# 4. Обработка/Хэндлер на любые сообщения
@dp.message()
async def send_echo(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text 
    logging.info(f'{user_name} {user_id}: {text}')
    await message.answer(text=translit(text))

# 5. Запуск процесса пуллинга
if __name__ == '__main__':
    dp.run_polling(bot)