import asyncio
import io
import logging
import threading
import time
from multiprocessing.context import Process

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputMediaDocument, KeyboardButton, ReplyKeyboardMarkup
from urllib.request import urlopen
import json
import sqlite3
#--------------------Настройки бота-------------------------

# Ваш токен от BotFather
TOKEN = '1327910681:AAFhevcF96T2SFrmvKYF_SxCrbEhT81IKWE'


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Ваш айди аккаунта администратора и айди сообщения где хранится файл с данными
admin_id=852450369
config_id=4
# conn = sqlite3.connect("mydb.db")  # или :memory: чтобы сохранить в RAM
# cursor = conn.cursor()


# #--------------------Получение данных-------------------------
async def get_data():
    to = time.time()
    # Пересылаем сообщение в данными от админа к админу
    forward_data = await bot.forward_message(admin_id, admin_id, config_id)

    # Получаем путь к файлу, который переслали
    file_data = await bot.get_file(forward_data.document.file_id)

    # Получаем файл по url
    file_url_data = bot.get_file_url(file_data.file_path)
    data_db=urlopen(file_url_data).read()
    # Считываем данные с файла
    f = open('minecraft.db', 'wb')
    f.write(data_db)
    f.close()
    print('Время получения бекапа :=' + str(time.time() - to))
    # Переводим данные из json в словарь и возвращаем



#--------------------Сохранение данных-------------------------
async def save_data():
    to = time.time()

    try:
        # Переводим словарь в строку
        f = open("minecraft.db", "rb")

        # Обновляем  наш файл с данными
        await bot.edit_message_media(InputMediaDocument(f), admin_id, config_id)

    except Exception as ex:
        print(ex)
    print('Время сохранения бекапа:='+str(time.time() - to))

#--------------------Метод при нажатии start-------------------------
@dp.message_handler(commands='start')
async def start(message: types.Message):
    # Добавляем нового пользователя
    await bot.send_message(message.chat.id,'Приветствую {}'.format(message.chat.first_name))



#--------------------Основная логика бота-------------------------
@dp.message_handler()
async def main_logic(message: types.Message):

    to=time.time()
# Логика для администратора
    if message.text == 'admin':
        # cursor.execute("CREATE TABLE stats_stats ( user_uuid uuid ,exp int, crystal int, money int,rating int, skin int,skin1 bool,skin2 bool,skin3 bool,skin4 bool,skin5 bool,skin6 bool,skin7 bool,skin8 bool,skin9 bool,skin10 bool,skin11 bool,skin12 bool,skin13 bool,skin14 bool,skin15 bool,skin16 bool,skin17 bool,skin18 bool,skin19 bool,skin20 bool)")
        # # cursor.execute("INSERT INTO users VALUES (1234, 'eee', 1,0)")
        # conn.commit()
        # # sql = "SELECT * FROM users "
        # # cursor.execute(sql)
        # # data = cursor.fetchall()
        # # str_data = json.dumps(data)
        f = open("minecraft.db", "rb")
        await bot.send_document(message.chat.id, f)
        await bot.send_message(message.chat.id, 'admin_id = {}'.format(message.chat.id))
        await bot.send_message(message.chat.id, 'config_id = {}'.format(message.message_id+1))
    print(time.time()-to)



def timer_start():
    threading.Timer(30.0, timer_start).start()
    time.sleep(3)
    try:
        asyncio.run_coroutine_threadsafe(save_data(),bot.loop)
    except Exception as exc:
        pass

def main_start():
    try:
        asyncio.run_coroutine_threadsafe(get_data(), bot.loop)
    except Exception as exc:
        pass

    timer_start()
    executor.start_polling(dp, skip_updates=True)

def proc_start():
    proc =  threading.Thread(target=main_start)
    proc.start()
#--------------------Запуск бота-------------------------
if __name__ == '__main__':
    try:
        asyncio.run_coroutine_threadsafe(get_data(), bot.loop)
    except Exception as exc:
        pass

    timer_start()
    executor.start_polling(dp, skip_updates=True)