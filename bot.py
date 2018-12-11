import telebot
from sql import DataBase
import keyboards
import requests
db = DataBase('Audio.sql')
#ip = '90.84.240.81'
#port = '3128'
furl_template = 'https://api.telegram.org/file/bot{}/{}'
#telebot.apihelper.proxy = {
#  'https': 'https://{}:{}'.format(ip,port)
#}
token = '768286581:AAF00PXpCi7YKlC_FjchUyAAB7ohQUEbS7w'
bot = telebot.TeleBot(token)
def description(message,file_id):
	try:
		cursor = db.cursor()
		db.add_file_id(message.from_user.id,file_id,message.text,cursor = cursor)
		print(message.from_user.id)
		bot.send_message(message.from_user.id,"Добавлено!")
	except Exception as e:
		print(e)
		bot.send_message(message.from_user.id,"Произошла ошибка, попробуйте позже")
def new(message):
	if message.voice:
		bot.send_message(message.from_user.id, "Напишите подсказку, по которой сможете найти сообщение.")
		bot.register_next_step_handler(message,lambda x: description(x,message.voice.file_id))
	elif message.audio:
		if message.audio.file_size <= 1024*1024 * 5:
			file_info = bot.get_file(message.audio.file_id)
			try:
				response = requests.get(furl_template.format(token,file_info.file_path))
				file = response.content
				voice = bot.send_voice(message.from_user.id,file).voice.file_id
				bot.send_message(message.from_user.id, "Напишите подсказку, по которой сможете найти сообщение.")
				bot.register_next_step_handler(message,lambda x: description(x,voice))
			except Exception as e:
				bot.send_message(message.from_user.id,"Произошла ошибка")
				print(furl_template.format(token,file_info.file_path))
		

@bot.message_handler(commands=['newvoice'])
def voice(message):
	voice = message.voice
	client_id = message.from_user.id
	bot.send_message(client_id,"Отправьте голосовое сообщение или аудио")
	bot.register_next_step_handler(message,new)


@bot.inline_handler(func = lambda query: True)
def empty_query(query):
	#print(query)
	client_id = query.from_user.id
	d = query.query
	data = db.search(client_id,d)
	articles = []
	for i,f in enumerate(data):
		a =  telebot.types.InlineQueryResultCachedVoice(id=str(i),title=f[1],voice_file_id=f[0],parse_mode='Markdown')
		articles.append(a)

	#a = telebot.types.InlineQueryResultArticle('1',"Title",description="description",input_message_content=telebot.types.InputTextMessageContent(message_text='text'))
	bot.answer_inline_query(query.id,articles)
	#print(2)
@bot.message_handler(commands=['voices'])
def get_voices(message):
	client_id = message.from_user.id
	data = db.get_voices(client_id)
	for i in data:
		bot.send_message(client_id,i['description'],reply_markup=keyboards.voice_menu(i['file_id']))
	if len(data) == 0:
		bot.send_message(client_id,"У вас нет ни одного голосового сообщения, добавьте его с помощью /newvoice")

@bot.callback_query_handler(func=lambda callback: callback.data.find('delete_') != -1 )
def delete(callback):
	file_id = callback.data.split('_')[-1]
	db.delete(file_id)
	bot.send_message(callback.from_user.id,"Удалено")
	bot.delete_message(callback.from_user.id,callback.message.message_id)
while True:
	try:
		bot.polling(none_stop=True)
	except:
		print('error')