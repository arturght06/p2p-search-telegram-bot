from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from connect import print_all_price
import asyncio



button_cancel = KeyboardButton('Назад')


async def res_key():
	list_prices = await print_all_price()
	res_key = ReplyKeyboardMarkup(resize_keyboard=True)
	a = [str(I+1) for I in range(len(list_prices))]
	res_key.add(*a)
	res_key.row(button_cancel)
	return res_key

# loop = asyncio.get_event_loop()
# res_key = loop.run_until_complete(res_key_func())
# res_key = ReplyKeyboardMarkup(resize_keyboard=True).add(*[str(I+1) for I in range(len(await print_all_price()))]).row(button_cancel)

button_complete = KeyboardButton('Готово✅')
complete_key = ReplyKeyboardMarkup(resize_keyboard=True).add(button_complete).add(button_cancel)



brcs_key = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)

button_my_id = KeyboardButton('Мій Id🎫')
button_time_sub = KeyboardButton('Скільки залишилось⌛️')
button_continue_sub = KeyboardButton('Купити підписку💸')
sub_key = ReplyKeyboardMarkup(resize_keyboard=True).add(button_time_sub, button_my_id).add(button_continue_sub).add(button_cancel)


button_subscribe = KeyboardButton('Підписка')
button_courses_spot = KeyboardButton('Курси SPOT')
button_spred_p2p_spot = KeyboardButton('Курси на SPOT та P2P')
button_courses_p2p = KeyboardButton('Курси P2P(конкретна біржа)')
button_allp2p = KeyboardButton('Курси P2P(Всі)')

#
#
#
#
#
#

button_p2p = KeyboardButton('P2P📈')
button_spot = KeyboardButton('Спот📈')
button_sub = KeyboardButton('Підписка🔑')
button_faq = KeyboardButton('FAQ📜')
button_all = KeyboardButton('Разом🔗')

# greet_key = ReplyKeyboardMarkup(resize_keyboard=True).row(button_spred_p2p_spot, button_courses_spot).row(button_courses_p2p, button_allp2p).row(button_subscribe)
greet_key = ReplyKeyboardMarkup(resize_keyboard=True).row(button_p2p, button_spot).row(button_all, button_faq)


button_p2p_all = KeyboardButton('Курси P2P(Всі)📋')
button_p2p_one = KeyboardButton('Ордери на біржі🧾')

p2p_key = ReplyKeyboardMarkup(resize_keyboard=True).row(button_p2p_all, button_p2p_one).row(button_cancel)


button_binance = KeyboardButton('▪️ Binance ▪️')
button_huobi = KeyboardButton('▪️ Huobi ▪️')
button_bybit = KeyboardButton('▪️ Bybit ▪️')

excgs_key = ReplyKeyboardMarkup(resize_keyboard=True).row(button_binance, button_bybit).row(button_cancel)



#
#
#
#
#
#

button_login = KeyboardButton("Увійти")

login_key = ReplyKeyboardMarkup(resize_keyboard=True).row(button_login)


button_buy = KeyboardButton('Купити🟢')
button_sell = KeyboardButton('Продати🔴')

buy_sell_key = ReplyKeyboardMarkup(resize_keyboard=True).row(button_buy, button_sell).add(button_cancel)


button_next = KeyboardButton('Пропустити')

next_key = ReplyKeyboardMarkup(resize_keyboard=True).add(button_next).add(button_cancel)


button_add_user = KeyboardButton('Додати')
button_delete_user = KeyboardButton('Видалити')
button_check_user = KeyboardButton('Перевірити інфо')
button_check_all = KeyboardButton('Список акаунтів')
button_prices = KeyboardButton('Ціни на підписку')
button_delete_price = KeyboardButton('Видалити ціну')
button_add_price = KeyboardButton('Додати ціну')


admin_key = ReplyKeyboardMarkup(resize_keyboard=True).add(button_add_user, button_delete_user).add(button_check_user, button_check_all).add(button_prices, button_delete_price, button_add_price).add(button_cancel)


