from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types, Dispatcher
from keyboard import greet_key, brcs_key, sub_key, res_key, complete_key
from config import admin_id
import time
from datetime import datetime
from connect import get_info_db, check, print_all_price


# ean = barcode.get('ean13', barcode_init, writer=ImageWriter())
            


'''
functions(hendlers)
'''
class FSMcreate(StatesGroup):
    checking = State()
    cont = State()
    complete = State()

async def sub_start(message: types.Message):
	print(str(f'LOG --- User {message.from_user} asked his time'))
	await FSMcreate.checking.set()
	await bot.send_message(chat_id = message.from_user.id, text = "<b><i>☑️ Обирай функцію ⚙️</i></b>" , reply_markup=sub_key)

async def user_id_getter(message: types.Message):
	print(str(f'LOG --- User {message.from_user} asked his time'))
	await bot.send_message(chat_id = message.from_user.id, text = f"<b><i>👉Ось твій Id для підписки:</i></b> <code>{message.from_user.id}</code>")

async def checker_time(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    end_time = await get_info_db(str(user_id))
    print(end_time, user_id)
    if end_time >= int(time.time()):
        real_time = int(time.time())
        print(real_time)
        if end_time >= real_time:
            dat = datetime.fromtimestamp(end_time).strftime('%d-%m-%Y \n%Hгод. %Mхв.')
            data = f'⏳<i><b>Підписка cкінчиться:</b></i>\n<b>{dat}</b>'
    else:
        data = f'<b>Підписка відсутня🩸</b>\n(за подовженням дії пиши: @dimadefy)'
    await bot.send_message(chat_id=message.from_user.id, text=f'{data}')


#
#
#

async def continue_sub(message: types.Message, state: FSMContext):
    list_subs = await print_all_price()
    result_string_list = "☑️ <i><b>Обери тип підписки що цікавить і напиши її номер </b></i>👇\n"
    inx = 1
    for i in list_subs:
        result_string_list += f'▪️ Номер {inx}: <i>на</i> <b>{i}</b> <i>дні за</i> <b>{list_subs.get(i)}</b>\n'
        inx += 1

    await bot.send_message(chat_id=message.from_user.id, text = f"{result_string_list}", reply_markup=await res_key())
    await FSMcreate.cont.set()

async def sub_sender(message: types.Message, state: FSMContext):
    try:
        dict_subs = dict(await print_all_price())
        price = [(x, dict_subs.get(x)) for x in dict_subs]
        print(price[int(message.text)-1])
        dat = datetime.fromtimestamp(int(time.time()) + (int(price[int(message.text)-1][0]) * 86400) + 10800).strftime('%Y %m %d %H:%M')
        await bot.send_message(chat_id=message.from_user.id, text=
f'''💸 <i>До сплати: <b>{price[int(message.text)-1][1]}</b> ₴

👉 Для сплати треба поповнити <b>банку Monobank</b> за посиланням нижче
👉 В коментар додай свiй id - <code>{message.from_user.id}</code>, щоб ми могли швидше все перевiрити</i>
https://send.monobank.ua/jar/4wbdHDhyeK

<i>👇 Наостанок напиши точний час транзакції для уточнення</i>''', reply_markup=brcs_key)
        await FSMcreate.complete.set()
        async with state.proxy() as data:
            data['result'] = f'Користувач {message.from_user} сплатив {price[int(message.text)-1][1]} за {message.text} тарифом.\nГотовий текст для додавання в адмін панелі - <code>{message.from_user.id} {dat}</code>'
    except:
        await bot.send_message(chat_id=message.from_user.id, text='<i><b>Щось не так🤔\nСпробуй ще раз❗️</b></i>')
        print('faillllll')

async def complete(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        result = data['result']

    await bot.send_message(chat_id=-1001551885182, text=f'❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️\n{result}\nЧас транзакції: {message.text}\n❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️')
    await bot.send_message(chat_id=5439961997, text=f'❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️\n{result}\nЧас транзакції: {message.text}\n❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️')
    await bot.send_message(chat_id=message.from_user.id, text=f'<i><b>Готово✅\nОчікуй повідомлення про підтвердження тут 😉</b></i>', reply_markup=greet_key)
    await state.finish()

#
#
#



async def back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(chat_id = message.from_user.id, text = 'Ok', reply_markup=greet_key)

def register_handlers_create(dp: Dispatcher):
    dp.register_message_handler(back, state='*', commands=['Назад'])
    dp.register_message_handler(back, Text(equals='назад', ignore_case=True), state='*')
    dp.register_message_handler(sub_start, text=["Підписка🔑"], state = None)
    dp.register_message_handler(continue_sub, text=['Купити підписку💸'], state = FSMcreate.checking)
    dp.register_message_handler(user_id_getter, text=["Мій Id🎫"], state = FSMcreate.checking)
    dp.register_message_handler(checker_time, text=["Скільки залишилось⌛️"], state = FSMcreate.checking)
    dp.register_message_handler(sub_sender, state = FSMcreate.cont)
    dp.register_message_handler(complete, state = FSMcreate.complete)
