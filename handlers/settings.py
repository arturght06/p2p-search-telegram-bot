from keyboard import greet_key, login_key
from aiogram import Dispatcher
from create_bot import dp, bot 
from config import admin_id
from api import price_Binance
from connect import write, check
import time

# @dp.message_handler(commands=['start'])
async def process_hi_command(message):
    print(str(f'LOG --- Такой пользователь запустил бота{message.from_user}'))
    for i in admin_id:
        await bot.send_message(chat_id=i,  text=str(f'LOG --- Такой пользователь запустил бота{message.from_user}'))
    #await message.answer_sticker(r'CAACAgQAAxkBAAEDy5Fh-x-svmcxY5AZKtmbD1ey64QiwAACiAADLOlYDEVV-cLQgV_2IwQ')
    await bot.send_message(chat_id=message.from_user.id, text='Вітаю друже, мене звати\n <i>king👑p2p bot🤖</i>\nІ я допоможу тобі заробити на р2р-обмінах 💰\nПочнемо 😎👇', reply_markup=greet_key)
    if await check(str(message.from_user.id)) is not True:
        t = int(time.time()) -10
        await write(str(message.from_user.id), t)

def register_handlers_settings(dp: Dispatcher):
    dp.register_message_handler(process_hi_command, text = ['Назад', '/start'])
    # dp.register_message_handler(process_hi_command, text = ['Увійти'])
    # dp.register_message_handler(echo)