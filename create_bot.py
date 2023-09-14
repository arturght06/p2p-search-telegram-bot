from aiogram import Bot, Dispatcher
from config import token, admin_id
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

loop = asyncio.get_event_loop()
bot = Bot(token, parse_mode="HTML")
dp = Dispatcher(bot, loop=loop, storage = storage)