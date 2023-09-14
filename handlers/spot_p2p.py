from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types, Dispatcher
from keyboard import greet_key, brcs_key, buy_sell_key, next_key
from config import admin_id
from string_maker import allP2Pprices
from connect import check


class FSMcreate(StatesGroup):
    token3 = State()
    additionally3 = State()

async def start_message_spotP2P(message: types.Message, state: FSMContext):
	#print(str(f'LOG --- Користувач {message.from_user} запитав курс'))

	if await check(str(message.from_user.id)):
		await FSMcreate.token3.set()
		await bot.send_message(chat_id = message.from_user.id, text = "☑️<b><i> Напиши торгову пару👇\n🔸 Наприклад: </i></b><code>Usdt uah</code>" , reply_markup=brcs_key)
	else:
		await bot.send_message(chat_id = message.from_user.id, text = 'Підписка відсутня\nПридбати\\подовжити, у підтримку👉@dimadefy', reply_markup=greet_key)

async def token_finder_spotP2P(message: types.Message, state: FSMContext):
	try:
		s1, s2 = str(message.text).split(' ')
		s1 = s1.upper()
		s2 = s2.upper()
		async with state.proxy() as data:
			data['s1'] = s1
			data['s2'] = s2
		print(s1, s2)

		await FSMcreate.additionally3.set()
		await bot.send_message(chat_id=message.from_user.id, text=f'<b><i>☑️ Додаткова інформація👇</i></b>\n<i>🔘 Можеш через пропуск додати (щось одне або разом):\n👉 Який метод оплати(наприклад: Monobank...)\n👉 Який об\'єм (наприклад: 1000)\n\n<b>💡Якщо не зважати на це, тоді натисни "Пропустити"💡</b></i>', reply_markup=next_key)
	except:
		await bot.send_message(chat_id=message.from_user.id, text=f'<i><b>Щось не так🤔\nСпробуй ще раз❗️</b></i>')
		
async def additionally_info(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		s1 = data['s1']
		s2 = data['s2']

	if str(message.text) == 'Пропустити':
		result_message = str(await allP2Pprices(s1, s2, '', '')).replace('#', '')
		await bot.send_message(chat_id=message.from_user.id, text=f'{str(result_message)}', reply_markup=greet_key)
		await FSMcreate.token3.set()
		await bot.send_message(chat_id = message.from_user.id, text = "☑️<b><i> Напиши торгову пару👇\n🔸 Наприклад: </i></b><code>Usdt uah</code>" , reply_markup=brcs_key)
	else:
		try:
			arr = str(message.text).split(' ')
			if len(arr) == 1:
				result_message = str(await allP2Pprices(s1, s2, arr[0])).replace('#', '')
				await bot.send_message(chat_id=message.from_user.id, text=f'{str(result_message)}', reply_markup=greet_key)
				await FSMcreate.token3.set()
				await bot.send_message(chat_id = message.from_user.id, text = "☑️<b><i> Напиши торгову пару👇\n🔸 Наприклад: </i></b><code>Usdt uah</code>" , reply_markup=brcs_key)
			elif len(arr) == 2:
				result_message = str(await allP2Pprices(s1, s2, arr[0], arr[1])).replace('#', '')
				await bot.send_message(chat_id=message.from_user.id, text=f'{str(result_message)}', reply_markup=greet_key)
				await FSMcreate.token3.set()
				await bot.send_message(chat_id = message.from_user.id, text = "☑️<b><i> Напиши торгову пару👇\n🔸 Наприклад: </i></b><code>Usdt uah</code>" , reply_markup=brcs_key)
		except:
			await bot.send_message(chat_id=message.from_user.id, text=f'<i><b>Щось не так🤔\nСпробуй ще раз❗️</b></i>', reply_markup=brcs_key)







async def back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(chat_id = message.from_user.id, text = 'Ok', reply_markup=greet_key)

def register_handlers_create(dp: Dispatcher):
    dp.register_message_handler(back, state='*', commands=['Назад'])
    dp.register_message_handler(back, Text(equals='назад', ignore_case=True), state='*')
    dp.register_message_handler(start_message_spotP2P, text=["Разом🔗"], state = None)
    dp.register_message_handler(token_finder_spotP2P, state = FSMcreate.token3)
    dp.register_message_handler(additionally_info, state = FSMcreate.additionally3)
