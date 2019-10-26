from __future__ import unicode_literals
import youtube_dl
import misc
import glob 
import os
from sys import argv
import telebot
import json
from time import sleep
import requests

global last_update_id 
last_update_id = 0
TOKEN = misc.token
bot = telebot.TeleBot(TOKEN)

URL = 'https://api.telegram.org/bot' + TOKEN + '/'

# Download data and config

download_options = {
	'format': 'bestaudio/best',
	'outtmpl': '%(title)s.%(ext)s',
	'nocheckcertificate': True,
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
	}],
}

# Song Directory
if not os.path.exists('Songs'):
	os.mkdir('Songs')
else:
	os.chdir('Songs')




def send_audio(files, text = 'ПАДАЖи ....'):
	global chat_id
	for i in files:
		lf = files[0]
		
		audio = open(i, 'rb')
		
		bot.send_audio(chat_id, audio)
	
	
# Download Songs

def skachat():

	global chat_id
	global text
	with youtube_dl.YoutubeDL(download_options) as dl:
		if 'playlist' in text:
			bot.send_message(chat_id,'skachivau playlist')
		else:
			bot.send_message(chat_id,'skachivau trek')
		dl.download([text])
		bot.send_message(chat_id,"fail skachan")
		shlyah = r'C:\\pybot\\Songs' + r'\\' + str(chat_id)
		files_path = os.path.join(shlyah, '*')
		files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True)
		send_audio(files)
		for i in files:
		    os.remove(i)
		


def get_updates():
	url = URL + 'getupdates'
	r = requests.get(url)
	return r.json()

def get_message():
	while True:
		data = get_updates()
		if data != "":
			last_object = data['result'][-1]
			current_update_id = last_object['update_id']
			global last_update_id
			if last_update_id != current_update_id: 
				last_update_id = current_update_id
				chat_id = last_object['message']['chat']['id']
				message_text = last_object['message']['text']
				message = {'chat_id': chat_id,
					   'message_text': message_text}
				return message
				get_updates()
				data = None
			return None
		else :
			sleep(1)
		

def send_message(chat_id, text = 'ПАДАЖи ....'):
	url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
	requests.get(url)

def main():
	while True:
		answer = get_message()
		if answer != None:
			global chat_id
			chat_id = answer['chat_id']
			global text
			text = answer['message_text']
			message = {'chat_id': chat_id,
				   'message_text': text}
			if 'youtube' in text or 'youtu.be' in text:
				#Create or select directory
				if not os.path.exists(r'C:\\pybot\\Songs' + r'\\' + str(chat_id)):
					os.mkdir(r'C:\\pybot\\Songs' + r'\\' + str(chat_id))
					os.chdir(r'C:\\pybot\\Songs' + r'\\' + str(chat_id))
				else:
					os.chdir(r'C:\\pybot\\Songs' + r'\\' + str(chat_id))
				skachat()
			elif text == '/start':
				send_message(chat_id, 'Добро пожаловать в YOUK Bot👋.\n\n Если Вы используете смартфон \n 1.В YouTube с телефона нажмите стрелочку "Поделиться". \n 2.Из предложеного списка выбирете Telegram. \n 3.Выбирете бота и просто отправьте ему сообщение. \n Если Вы используете компьютер\n 1.Cкопируйте ссылку из адресного поля браузера, или нажмите \nстрелочку "Поделиться".\n 2.Скопируйте ссылку оттуда.\n 3.Отправьте боту. \n\n Загрузив трек один раз, больше не придется видеть\n уведомление: "Фоновое прослушивание музыки ограничено",\n или рекламу посреди прослушивания трека.\n Скачанные аудиозаписи будут доступны для прослушивания\nдаже если у вас кончился трафик, или отсутствует интернет. ')
		else :
			continue

if __name__ == '__main__':
	main()

##https://music.youtube.com/playlist?list=PLSxz4KA_b1INvxkCglrRvqI7EOLGC_iqW
##https://music.youtube.com/watch?v=kPtiZM6tqaM&feature=share
