from keyboard import greet_key, login_key
from aiogram import Dispatcher
from create_bot import dp, bot 
from config import admin_id
from api import price_Binance

# @dp.message_handler(commands=['start'])
async def process_hi_command(message):
    await bot.send_message(chat_id=message.from_user.id, text='''
<b>👋 Привіт</b>
<i>Я - Перший україномовний бот-помічник для торгівлі на P2P та арбітражі криптою 😉
Цей бот розроблений спеціально для P2P-трейдерів/арбітраж-ників криптовалютою
</i>
<b>Швидкий пошук 🏎
Зрозумілий інтерфейс⌨️
Все це про мене🔥</b>

<i>Якщо в тебе з'являться питання про мене, то підтримка залюбки тобі допоможе😉❤️
Можеш писати нам не тільки питання, але й твої особисті побажання, якісь помилки по боту.</i> 
<b>Розробник 👉 @netut_true 😊</b>''', reply_markup=greet_key)


def register_handlers_create(dp: Dispatcher):
    dp.register_message_handler(process_hi_command, text = ['FAQ📜'])