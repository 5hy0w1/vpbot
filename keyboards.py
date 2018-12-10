from telebot import types
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton

def voice_menu(file_id):
	keyboard = InlineKeyboardMarkup(row_width=2)
	delete = InlineKeyboardButton(text = 'Удалить',callback_data='delete_{}'.format(file_id))
	change_description = InlineKeyboardButton(text = 'Изменить описание',callback_data='change_{}'.format(file_id))
	keyboard.add(delete,change_description)
	return keyboard