from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types, Dispatcher
from keyboard import greet_key, brcs_key, p2p_key, buy_sell_key, next_key,  excgs_key
from config import admin_id
from all_p2p import infoOfAllExchanges, infoOfAllExchanges_p2p_one
from connect import check

class FSMcreate(StatesGroup):
    p2p_panel = State()
    buy_sell = State()
    token = State()
    additionally = State()

    exchanges = State()
    token2 = State()
    additionally2 = State()
    buy_sell2 = State()


async def p2p_panel_start(message: types.Message):
	if await check(str(message.from_user.id)):
		await FSMcreate.p2p_panel.set()
		await bot.send_message(chat_id = message.from_user.id, text = "🔹<b>В цьому розділі можна подивитись:</b>\n👉 курси P2P на біржах (коротко на кожній)\n👉 список ордерів на конкретній біржі\n\n💡<i><b>Обирай що цікавить</b></i>👇" , reply_markup=p2p_key)
	else:
		await bot.send_message(chat_id = message.from_user.id, text = 'Підписка відсутня\nПридбати\\подовжити, у підтримку👉@dimadefy', reply_markup=greet_key)


#
#
#
#
#
#


async def start_message(message: types.Message, state: FSMContext):
	await FSMcreate.buy_sell.set()
	await bot.send_message(chat_id = message.from_user.id, text = "<i><b>☑️ Обери тип транзакції👇</b></i>" , reply_markup=buy_sell_key)

async def buy_sell_choosing(message: types.Message, state: FSMContext):
	# s1, s2 = message.split(' ')
	if str(message.text) == 'Купити🟢':
		buy_sell = 'BUY'
	elif str(message.text) == 'Продати🔴':
		buy_sell = 'SELL'

	async with state.proxy() as data:
		data['buy_sell'] = buy_sell

	await FSMcreate.token.set()
	await bot.send_message(chat_id=message.from_user.id, text=f'☑️<b><i> Напиши торгову пару👇\n🔸 Наприклад: </i></b><code>Usdt uah</code>', reply_markup=brcs_key)

async def token_finder(message: types.Message, state: FSMContext):
	try:
		s1, s2 = str(message.text).split(' ')
		s1 = s1.upper()
		s2 = s2.upper()
		async with state.proxy() as data:
			data['s1'] = s1
			data['s2'] = s2
		print(s1, s2)

		await FSMcreate.additionally.set()
		await bot.send_message(chat_id=message.from_user.id, text=f'<b><i>☑️ Додаткова інформація👇</i></b>\n<i>🔘 Можеш через пропуск додати (щось одне або разом):\n👉 Який метод оплати(наприклад: Monobank...)\n👉 Який об\'єм (наприклад: 1000)\n\n<b>💡Якщо не зважати на це, тоді натисни "Пропустити"💡</b></i>', reply_markup=next_key)
	except:
		await bot.send_message(chat_id=message.from_user.id, text=f'<i><b>Щось не так🤔\nСпробуй ще раз❗️</b></i>')
		
async def additionally_info(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		s1 = data['s1']
		s2 = data['s2']
		buy_sell = data['buy_sell']

	if str(message.text) == 'Пропустити':
		result_message = await infoOfAllExchanges(True, s1, s2, buy_sell)
		await bot.send_message(chat_id=message.from_user.id, text=f'{result_message}', reply_markup=buy_sell_key)
		await FSMcreate.buy_sell.set()
	else:
		try:
			arr = str(message.text).split(' ')
			if len(arr) == 1:
				result_message = await infoOfAllExchanges(True, s1, s2, buy_sell, arr[0])
				await bot.send_message(chat_id=message.from_user.id, text=f'{result_message}', reply_markup=buy_sell_key)
				await FSMcreate.buy_sell.set()
			elif len(arr) == 2:
				result_message = await infoOfAllExchanges(True, s1, s2, buy_sell, arr[0], arr[1])
				await bot.send_message(chat_id=message.from_user.id, text=f'{result_message}', reply_markup=buy_sell_key)
				await FSMcreate.buy_sell.set()
		except:
			await bot.send_message(chat_id=message.from_user.id, text=f'<i><b>Щось не так🤔\nСпробуй ще раз❗️</b></i>', reply_markup=brcs_key)
#
#
#
#
#

async def start_message_p2p_exgs(message: types.Message, state: FSMContext):
	await FSMcreate.exchanges.set()
	await bot.send_message(chat_id = message.from_user.id, text = "<b><i>☑️ Обери біржу👇</i></b>" , reply_markup=excgs_key)

async def exchg_choosing(message: types.Message, state: FSMContext):
	# s1, s2 = message.split(' ')
	if str(message.text) == '▪️ Binance ▪️':
		exchg = 1
	# elif str(message.text) == '▪️ Huobi ▪️':
	# 	exchg = 2
	elif str(message.text) == '▪️ Bybit ▪️':
		exchg = 3


	async with state.proxy() as data2:
		data2['exchg'] = exchg

	await FSMcreate.buy_sell2.set()
	await bot.send_message(chat_id=message.from_user.id, text=f"<b><i>☑️ Обери тип транзакції👇</i></b>" , reply_markup=buy_sell_key)

async def buy_sell_choosing2(message: types.Message, state: FSMContext):
	# s1, s2 = message.split(' ')
	if str(message.text) == 'Купити🟢':
		buy_sell = 'BUY'
	elif str(message.text) == 'Продати🔴':
		buy_sell = 'SELL'

	async with state.proxy() as data2:
		data2['buy_sell'] = buy_sell

	await FSMcreate.token2.set()
	await bot.send_message(chat_id=message.from_user.id, text=f'☑️<b><i> Напиши торгову пару👇\n🔸 Наприклад: </i></b><code>Usdt uah</code>', reply_markup=brcs_key)

async def token_finder2(message: types.Message, state: FSMContext):
	try:
		s1, s2 = str(message.text).split(' ')
		s1 = s1.upper()
		s2 = s2.upper()
		async with state.proxy() as data2:
			data2['s1'] = s1
			data2['s2'] = s2
		print(s1, s2)

		await FSMcreate.additionally2.set()
		await bot.send_message(chat_id=message.from_user.id, text=f'<b><i>☑️ Додаткова інформація👇</i></b>\n<i>🔘 Можеш через пропуск додати (щось одне або разом):\n👉 Який метод оплати(наприклад: Monobank...)\n👉 Який об\'єм (наприклад: 1000)\n\n<b>💡Якщо не зважати на це, тоді натисни "Пропустити"💡</b></i>', reply_markup=next_key)
	except:
		await bot.send_message(chat_id=message.from_user.id, text=f'<i><b>Щось не так🤔\nСпробуй ще раз❗️</b></i>')

async def additionally_info2(message: types.Message, state: FSMContext):
	async with state.proxy() as data2:
		s1 = data2['s1']
		s2 = data2['s2']
		exchg = data2['exchg']
		buy_sell = data2['buy_sell']

	if str(message.text) == 'Пропустити':
		result_message = await infoOfAllExchanges_p2p_one(s1, s2, buy_sell, exchg)
		await bot.send_message(chat_id=message.from_user.id, text=f'{result_message}', reply_markup=excgs_key)
		await FSMcreate.exchanges.set()
	else:
		try:
			arr = str(message.text).split(' ')
			if len(arr) == 1:
				result_message = await infoOfAllExchanges_p2p_one(s1, s2, buy_sell, exchg, arr[0])
				await bot.send_message(chat_id=message.from_user.id, text=f'{result_message}', reply_markup=excgs_key)
				await FSMcreate.exchanges.set()
			elif len(arr) == 2:
				result_message = await infoOfAllExchanges_p2p_one(s1, s2, buy_sell, exchg, arr[0], arr[1])
				await bot.send_message(chat_id=message.from_user.id, text=f'{result_message}', reply_markup=excgs_key)
				await FSMcreate.exchanges.set()
		except:
			await bot.send_message(chat_id=message.from_user.id, text=f'<i><b>Щось не так🤔\nСпробуй ще раз❗️</b></i>', reply_markup=brcs_key)


async def back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    # print(str(current_state))
    if current_state is None:
    	return
    elif str(current_state) in ["FSMcreate:buy_sell", "FSMcreate:p2p_all_currency", "FSMcreate:token", "FSMcreate:additionally"]:
    	await FSMcreate.p2p_panel.set()
    	await bot.send_message(chat_id = message.from_user.id, text = 'Ok', reply_markup=p2p_key)
    	return
    else:
    	await state.finish()
    	await bot.send_message(chat_id = message.from_user.id, text = 'Ok', reply_markup=greet_key)
    	return

def register_handlers_create(dp: Dispatcher):
    dp.register_message_handler(back, state='*', commands=['Назад'])
    dp.register_message_handler(back, Text(equals='назад', ignore_case=True), state='*')
    dp.register_message_handler(p2p_panel_start, text=["P2P📈"], state = None)
    # All currency of all exchanges
    dp.register_message_handler(start_message, text=["Курси P2P(Всі)📋"], state = FSMcreate.p2p_panel)
    dp.register_message_handler(buy_sell_choosing, text=['Продати🔴', 'Купити🟢'], state = FSMcreate.buy_sell)
    dp.register_message_handler(token_finder, state = FSMcreate.token)
    dp.register_message_handler(additionally_info, state = FSMcreate.additionally)
    # All offers on the same exchange
    dp.register_message_handler(start_message_p2p_exgs, text=["Ордери на біржі🧾"], state = FSMcreate.p2p_panel)
    dp.register_message_handler(exchg_choosing, text=['▪️ Binance ▪️', '▪️ Huobi ▪️', '▪️ Bybit ▪️'], state = FSMcreate.exchanges)
    dp.register_message_handler(buy_sell_choosing2, text=['Продати🔴', 'Купити🟢'], state = FSMcreate.buy_sell2)
    dp.register_message_handler(token_finder2, state = FSMcreate.token2)
    dp.register_message_handler(additionally_info2, state = FSMcreate.additionally2)



