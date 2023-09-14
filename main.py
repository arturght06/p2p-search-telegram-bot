from config import admin_id
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import aioschedule
import keyboard
from create_bot import bot, dp
from api import pricesString, prices
from time import sleep
# from handlers.admin import post_in_channel

async def start_mailing():
    prices_mess = ((await pricesString('USDT', 'UAH', prices)).split('\n🔥')[0]).split('немає пари❄')[0]
    prices_mess = '📊USDT/UAH\n' + ('\n'.join(prices_mess.split('\n')[:-1]))
    await bot.send_message(chat_id=-1001740667886, text=prices_mess)


async def scheduler():
    #aioschedule.every().minutes.do(start_mailing)
    aioschedule.every().day.at("9:00").do(start_mailing)
    aioschedule.every().day.at("17:00").do(start_mailing)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def send_admin(dp):
    # asyncio.create_task(scheduler())
    for i in admin_id:
        await bot.send_message(chat_id = i, text = "Bot was started")
    await bot.send_message(chat_id=-1001551885182, text="Bot was started")
    
    # while True:
    #     await post_in_channel(dp)

    #     await asyncio.sleep(10)

from handlers import settings, subs, spot_p2p, admin, p2p, spot, faq

settings.register_handlers_settings(dp)
admin.register_handlers_create(dp)
p2p.register_handlers_create(dp)
subs.register_handlers_create(dp)
spot.register_handlers_create(dp)
spot_p2p.register_handlers_create(dp)
faq.register_handlers_create(dp)



executor.start_polling(dp, on_startup=send_admin, skip_updates=True)
