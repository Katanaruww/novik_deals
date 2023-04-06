#code by: phantom_off
import sqlite3
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import time
import sys
import subprocess
storage = MemoryStorage()


class FSM(StatesGroup):
	token = State()
	rekv = State()

bot = Bot("5963298629:AAFj_5KaqmF8FYVqcmmo-Btkpn4hoC__L34")
dp = Dispatcher(bot, storage=storage)
admins = [6035428327, 6207847020]
supp = "[Разработка: Phantom]"
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


ma = InlineKeyboardMarkup()
ma.add(InlineKeyboardButton("Добавить карту", callback_data="on_check"))
ma.add(InlineKeyboardButton("Добавить токен", callback_data="add_token"))
ma.add(InlineKeyboardButton("Просмотр карт", callback_data="see_cards"))
ma.add(InlineKeyboardButton("Выбор действия", callback_data="change"))
ma.add(InlineKeyboardButton("Поддержка", callback_data="help"))

@dp.message_handler(commands=["start"], state=None)
async def start(message):
	if message.chat.id in admins:
		await bot.send_message(message.chat.id, "<b>Привет!</b>",
							   parse_mode="HTML", reply_markup=ma)
@dp.callback_query_handler(lambda call: call.data == "del_card", state="*")
async def delete(call, state: FSMContext):
	
	current_state = await state.get_data()
	if current_state is None:
		return
	await state.finish()
	x = conn.execute("SELECT id_cards FROM cards ORDER BY id DESC LIMIT 1").fetchone()
	cursor.execute("DELETE FROM cards WHERE id_cards = ?", (x[0],))
	conn.commit()
	await call.message.edit_text("<b>🚫ОТМЕНЕНО🚫\n\n</b>", parse_mode="HTML", reply_markup=ma)
@dp.callback_query_handler(lambda call: call.data and call.data.startswith("smotr_"))
async def delete(call):

	x = call.data.replace("smotr_", "")
	row = cursor.execute("SELECT * FROM cards WHERE id_cards = ?", (x,)).fetchone()
	mar = InlineKeyboardMarkup()
	mar.add(InlineKeyboardButton("Удалить🚫", callback_data=f"delete_{row[3]}"))
	mar.add(InlineKeyboardButton("Назад👈", callback_data="see_cards"))

	await call.message.edit_text(f"<b>Тип оплаты: {row[1]}</b>\n"
								 f"<b>Реквизиты: {row[2]}</b>", parse_mode="HTML", reply_markup=mar)

@dp.callback_query_handler(lambda call: call.data and call.data.startswith("delete_"))
async def delete(call):
	x = call.data.replace("delete_", "")
	cursor.execute("DELETE  FROM cards WHERE id_cards = ?", (x,))
	conn.commit()
	mar = InlineKeyboardMarkup()
	mar.add(InlineKeyboardButton("Назад👈", callback_data="see_cards"))
	await call.message.edit_text(f"<b>Успешно!</b>", parse_mode="HTML", reply_markup=mar)
@dp.callback_query_handler(lambda call: True)
async def ca(call):
	if call.data == "on_check":
		card = InlineKeyboardMarkup()
		card.add(InlineKeyboardButton("Сбербанк", callback_data="add_sber"))
		card.add(InlineKeyboardButton("Qiwi", callback_data="add_qiwi"))
		card.add(InlineKeyboardButton("Перевод на карту", callback_data="add_perev_card"))
		card.add(InlineKeyboardButton("Мобильная связь", callback_data="add_mobile"))
		card.add(InlineKeyboardButton("Тинькофф", callback_data="add_tink"))
		card.add(InlineKeyboardButton("СБП", callback_data="add_sbp"))
		card.add(InlineKeyboardButton("Qiwi-счёт", callback_data="add_qiwi_shet"))
		card.add(InlineKeyboardButton("Назад👈", callback_data="menu_inline"))
		await call.message.edit_text("<b>Выбери тип оплаты:</b>", parse_mode="HTML", reply_markup=card)
	elif call.data == "change":
		change = InlineKeyboardMarkup()
		change.add(InlineKeyboardButton("Включить✅", callback_data="on_proc"))
		change.add(InlineKeyboardButton("Назад👈", callback_data="menu_inline"))
		await call.message.edit_text("Выбрите действие: ", reply_markup=change)
	elif call.data == "on_proc":
		pit = InlineKeyboardMarkup().add(InlineKeyboardButton("Выключить🚫", callback_data="off_proc"))
		await call.message.edit_text("Успешно!✅", reply_markup=pit)
		subprocess.Popen(['python', 'proc.py'])
	elif call.data == "off_proc":
		subprocess.Popen(['python', 'proc.py']).terminate()
		await call.message.edit_text("Успешно✅", reply_markup=ma)
	elif call.data == "add_sber":
		name = "Сбербанк"
		id_bank = call.id
		cursor.execute("INSERT INTO cards (payment_type, id_cards) VALUES (?, ?)", (name, id_bank,))
		conn.commit()
		delete = InlineKeyboardMarkup().add(InlineKeyboardButton("Отмена👈", callback_data="del_card"))
		await call.message.edit_text("Напишите реквизиты которые будут видны конечному клиенту:\n\n" , parse_mode="HTML", reply_markup=delete)
		await FSM.rekv.set()
	elif call.data == "add_qiwi":
		name = "Qiwi"
		id_bank = call.id
		cursor.execute("INSERT INTO cards (payment_type, id_cards) VALUES (?, ?)", (name, id_bank,))
		conn.commit()
		delete = InlineKeyboardMarkup().add(InlineKeyboardButton("Отмена👈", callback_data="del_card"))
		await call.message.edit_text("Напишите реквизиты которые будут видны конечному клиенту:\n\n", parse_mode="HTML", reply_markup=delete)
		await FSM.rekv.set()
	elif call.data == "add_perev_card":
		name = "Перевод на карту"
		id_bank = call.id
		cursor.execute("INSERT INTO cards (payment_type, id_cards) VALUES (?, ?)", (name, id_bank,))
		conn.commit()
		delete = InlineKeyboardMarkup().add(InlineKeyboardButton("Отмена👈", callback_data="del_card"))
		await call.message.edit_text("Напишите реквизиты которые будут видны конечному клиенту:\n\n", parse_mode="HTML", reply_markup=delete)
		await FSM.rekv.set()
	elif call.data == "add_mobile":
		name = "Мобильная связь"
		id_bank = call.id
		cursor.execute("INSERT INTO cards (payment_type, id_cards) VALUES (?, ?)", (name, id_bank,))
		conn.commit()
		delete = InlineKeyboardMarkup().add(InlineKeyboardButton("Отмена👈", callback_data="del_card"))
		await call.message.edit_text("Напишите реквизиты которые будут видны конечному клиенту:\n\n", parse_mode="HTML", reply_markup=delete)
		await FSM.rekv.set()
	elif call.data == "add_tink":
		name = "Тинькофф"
		id_bank = call.id
		cursor.execute("INSERT INTO cards (payment_type, id_cards) VALUES (?, ?)", (name, id_bank,))
		conn.commit()
		delete = InlineKeyboardMarkup().add(InlineKeyboardButton("Отмена👈", callback_data="del_card"))
		await call.message.edit_text("Напишите реквизиты которые будут видны конечному клиенту:\n\n", parse_mode="HTML", reply_markup=delete)
		await FSM.rekv.set()
	elif call.data == "add_sbp":
		name = "СБП"
		id_bank = call.id
		cursor.execute("INSERT INTO cards (payment_type, id_cards) VALUES (?, ?)", (name, id_bank,))
		conn.commit()
		delete = InlineKeyboardMarkup().add(InlineKeyboardButton("Отмена👈", callback_data="del_card"))
		await call.message.edit_text("Напишите реквизиты которые будут видны конечному клиенту:\n\n", parse_mode="HTML", reply_markup=delete)
		await FSM.rekv.set()
	elif call.data == "add_qiwi_shet":
		name = "Qiwi-счёт"
		id_bank = call.id
		cursor.execute("INSERT INTO cards (payment_type, id_cards) VALUES (?, ?)", (name, id_bank,))
		conn.commit()
		delete = InlineKeyboardMarkup().add(InlineKeyboardButton("Отмена👈", callback_data="del_card"))
		await call.message.edit_text("Напишите реквизиты которые будут видны конечному клиенту:\n\n", parse_mode="HTML", reply_markup=delete)
		await FSM.rekv.set()
	elif call.data == "add_token":
		await call.message.edit_text("<b>Привет! \nДля начала работы мне нужен токен сайта: </b>",
							   parse_mode="HTML")
		await FSM.token.set()
	elif call.data == "see_cards":
		card = InlineKeyboardMarkup()
		card.add(InlineKeyboardButton("Сбербанк", callback_data="see_sber"))
		card.add(InlineKeyboardButton("Qiwi", callback_data="see_qiwi"))
		card.add(InlineKeyboardButton("Перевод на карту", callback_data="see_perev_card"))
		card.add(InlineKeyboardButton("Мобильная связь", callback_data="see_mobile"))
		card.add(InlineKeyboardButton("Тинькофф", callback_data="see_tink"))
		card.add(InlineKeyboardButton("СБП", callback_data="see_sbp"))
		card.add(InlineKeyboardButton("Qiwi-счёт", callback_data="see_qiwi_shet"))
		card.add(InlineKeyboardButton("Назад👈", callback_data="menu_inline"))
		await call.message.edit_text("<b>Выбери тип оплаты:</b>", parse_mode="HTML", reply_markup=card)
	elif call.data == "menu_inline":
		await call.message.edit_text("<b>Привет! \nДля начала работы мне нужен токен сайта: </b>",
							   parse_mode="HTML", reply_markup=ma)
	elif call.data == "see_sber":
		await see_cards(call, "Сбербанк")
	elif call.data == "see_qiwi":
		await see_cards(call, "Qiwi")
	elif call.data == "see_perev_card":
		await see_cards(call, "Перевод на карту")
	elif call.data == "see_mobile":
		await see_cards(call, "Мобильная связь")
	elif call.data == "see_tink":
		await see_cards(call, "Тинькофф")
	elif call.data == "see_sbp":
		await see_cards(call, "СБП")
	elif call.data == "see_qiwi_shet":
		await see_cards(call, "Qiwi-счёт")

@dp.message_handler(state=FSM.rekv)
async def num(message, state: FSMContext):
	rekv = message.text
	await state.update_data(rekv=rekv)
	data = await state.get_data()
	rekv_get = data.get('rekv')
	msg = message.chat.id
	row = cursor.execute("SELECT id FROM cards ORDER BY id DESC LIMIT 1").fetchone()
	cursor.execute("UPDATE cards SET card = ? WHERE id = ?",
				   (rekv_get,  row[0],))
	conn.commit()
	mar = InlineKeyboardMarkup()
	mar.add(InlineKeyboardButton("Назад⏪", callback_data="on_check"))
	await bot.send_message(msg, "Успешно✅", reply_markup=mar)
	await state.finish()
@dp.message_handler(state=FSM.token)
async def token(message, state: FSMContext):
	token = message.text
	await state.update_data(token=token)
	data = await state.get_data()
	token_get = data.get("token")
	conn.execute("INSERT INTO setting (token) VALUES (?)", (token_get, ))
	conn.commit()
	await bot.send_message(message.chat.id, "Отлично! \nМеню доступно! \nЧтобы бот полностью работал перейдите во вкладку 'Добавить карту'", reply_markup=ma)
	await state.finish()
async def see_cards(call, name_bank):
	row = cursor.execute("SELECT * FROM cards WHERE payment_type = ?", (name_bank,)).fetchall()
	markup = InlineKeyboardMarkup()
	for i in range(len(row)):
		markup.add(InlineKeyboardButton(f"{row[i][2]}", callback_data=f"smotr_{row[i][3]}"))
	markup.add(InlineKeyboardButton("Назад⏪", callback_data="menu_inline"))
	await call.message.edit_text("<b>Список всех действующих карт</b>", parse_mode="HTML", reply_markup=markup)
if __name__ == '__main__':
	try:
		executor.start_polling(dp)
	except Exception as e:
		time.sleep(5)
		print(e)



