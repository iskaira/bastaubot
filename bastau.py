#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from time import sleep
import datetime
from pytz import timezone
import telebot
import constants
import config
import dbworker
from database import SQLight
from database import MySQL

logger = telebot.logger

telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(constants.token)

def check_message(text, message):
	if (len(text.split())) < 1:
		bot.reply_to(message, '<b>Жауап қабылданбады, толығырақ жазыңыз! Сіздің жауабыңыз сала таңдап кетуіңізге мыңызы улкен.</b>',parse_mode = "HTML")
		return False
	return True
def zhukteu_batyrma():
	markup = telebot.types.InlineKeyboardMarkup()
	row_1 = [telebot.types.InlineKeyboardButton(text = "Материалдарды жүктеу", callback_data = 'zhukteuMaterial')]
	markup.row(*row_1)
	return markup
@bot.message_handler(commands=['start'])
def starting(message):
	markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True, row_width = 1)#, ,
	markup.row(telebot.types.KeyboardButton(text="Номер жіберу", request_contact=True))
	bot.send_message(message.from_user.id,'Қайырлы күн!\nБизнес Бастау кәсіпкерлік мектебінің сала таңдау чат ботына қош келдіңіз!\nБот арқылы сізге сала таңдауға көмек беретін боламыз!\nБоттың соңына дейін сізде сала таңдауға үлкен ойлар пайда болады.\nДайынсызба? Онда бастайық!\n\n\n«Номерді жіберу» батырмасын басыңыз'+u"\U0001F447",reply_markup=markup)
@bot.message_handler(content_types=['contact'])
def phone_number(message):
	phone_number = message.contact.phone_number
	#mysql_db = MySQL()
	db = SQLight()
	print(phone_number)
	#exists = mysql_db.select_users(phone_number) # Uncomment if needed 
	exists = True
	if (exists):
		if not db.check_user_exists(phone_number):
			db.register_user(message.from_user.id, phone_number, exists)
		ia_zhok = telebot.types.InlineKeyboardMarkup()
		row_1 = [telebot.types.InlineKeyboardButton("Салам бар",callback_data="salaБар")]
		row_2 = [telebot.types.InlineKeyboardButton("Қабілетімді анықтағым келеді",callback_data="salaЖоқ")]# ozgertu bot
		ia_zhok.row(*row_1)
		ia_zhok.row(*row_2)
		bot.send_message(message.from_user.id,"<a href='https://www.youtube.com/watch?v=OWJlNyZx08E'>Сала таңдауға жалпы шолу</a>",parse_mode = "HTML",reply_markup=ia_zhok)
		return
	bot.send_message(message.from_user.id,"<b>Кешіріңіз, сіз біздің базада тіркелмегенсіз.</b>",parse_mode = "HTML")
	return	
#

@bot.callback_query_handler(func=lambda call: call.data[:4] == 'sala')
def Ia_Jok(call):
	zhauap =  call.data[4:]
	db = SQLight()
	reply_markup = telebot.types.ReplyKeyboardRemove()
	if zhauap == 'Бар':
		db.update_sala(123,zhauap)
		bot.answer_callback_query(call.id, text="Күте тұрыңыз...")
		bot.send_message(call.from_user.id, "<a href='https://www.youtube.com/watch?v=lJ-7CODAQqc'>Саласы бар</a>", parse_mode = "HTML", reply_markup=zhukteu_batyrma())
		return
	bot.answer_callback_query(call.id, text="Күте тұрыңыз...")
	db.update_sala(123,zhauap)
	markup = telebot.types.InlineKeyboardMarkup()
	row_1 = [telebot.types.InlineKeyboardButton(text = "Саламды анықтағым келеді", callback_data = '#')]
	markup.row(*row_1)
	bot.send_message(call.from_user.id, "<a href='https://www.youtube.com/watch?v=uWRvrdOyBXA'>Салам бар, бірақ өзім білмеймін</a>", parse_mode = "HTML",reply_markup = markup)
	dbworker.set_state(call.from_user.id, config.States.kirispe_pikir.value)
	
@bot.callback_query_handler(func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.kirispe_pikir.value)
def kirispe_pikir(call):
	bot.answer_callback_query(call.id, text="Күте тұрыңыз...")
	bot.send_message(call.from_user.id, "<a href='https://www.youtube.com/watch?v=JXs9LmFDJOs'>Сылтаулар</a>", 	parse_mode = "HTML")
	bot.send_message(call.from_user.id, "<b>Егер сіздің сылтауыңыз осылардан өзгеше болса, төменге жазып жіберіңіз.</b>"+u"\U0001F447", parse_mode = "HTML") #, reply_markup=ia_menu())
	dbworker.set_state(call.from_user.id, config.States.syltaular.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.syltaular.value)
def syltaular(message):
	if check_message(message.text,message):
		print(message.text)
		syltaular = message.text #Сылтаулар
		db = SQLight()
		db.update_syltau(123,syltaular)
		bot.send_message(message.from_user.id, "<a href='https://www.youtube.com/watch?v=CTeRikeIcsQ'>1 Қадам</a>",parse_mode = "HTML")
		bot.send_message(message.from_user.id, "<b>Төменге нәтижесін жазыңыз</b>"+u"\U0001F447", parse_mode = "HTML") #, reply_markup=ia_menu())
		dbworker.set_state(message.chat.id, config.States.kadam_1_pikir.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.kadam_1_pikir.value)
def kadam_1_pikir(message):
	if check_message(message.text,message):
		print(message.text)
		kadam_1_pikir = message.text #1 Қадам пікір
		db = SQLight()
		db.update_kadam_1(123, kadam_1_pikir)

		markup = telebot.types.InlineKeyboardMarkup()
		row_1 = [telebot.types.InlineKeyboardButton(text = "Видеоларды жүктеу", callback_data = 'zhukteuVideo')]
		row_2 = [telebot.types.InlineKeyboardButton(text = "Келесі қадамға өту", callback_data = 'kadam_3')]
		markup.row(*row_1)
		markup.row(*row_2)
		bot.send_message(message.from_user.id, "<a href='https://www.youtube.com/watch?v=FX3Txp-j6V8'>2 Қадам</a>",parse_mode = "HTML",reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'kadam_3')
def kadam_3(call):
	bot.answer_callback_query(call.id, text="Күте тұрыңыз...")
	markup = telebot.types.InlineKeyboardMarkup()
	row_1 = [telebot.types.InlineKeyboardButton(text = "Өнім адамы", callback_data = 'Өнім адамы')]
	row_2 = [telebot.types.InlineKeyboardButton(text = "Сату адамы", callback_data = 'Сату адамы')]
	markup.row(*row_1)
	markup.row(*row_2)
	bot.send_message(call.from_user.id,"<a href='https://www.youtube.com/watch?v=k4kGURq9owI'>3 Қадам</a>",parse_mode = "HTML")
	bot.send_message(call.from_user.id, "<b>Сіз қайсысына жатасыз?</b>"+u"\U0001F447", parse_mode = "HTML",reply_markup = markup) #, reply_markup=ia_menu())

	dbworker.set_state(call.from_user.id, config.States.kadam_3_pikir.value)

@bot.callback_query_handler(func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.kadam_3_pikir.value)
def kadam_3_pikir(call):
	bot.answer_callback_query(call.id, text="Күте тұрыңыз...")
	kadam_3_pikir = call.data #3 Қадам пікір Onim,Satu adam
	db = SQLight()
	db.update_kadam_3(123, kadam_3_pikir)
	bot.send_message(call.from_user.id, "<a href='https://www.youtube.com/watch?v=CBpjXXj9an4'>4 Қадам</a>",parse_mode = "HTML")
	bot.send_message(call.from_user.id, "<b>Келесі қадамға өту үшін, пікір қалдырыңыз</b>"+u"\U0001F447", parse_mode = "HTML") #, reply_markup=ia_menu())
	dbworker.set_state(call.from_user.id, config.States.kadam_4_pikir.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.kadam_4_pikir.value)
def kadam_4_pikir(message):
	if check_message(message.text,message):
		kadam_4_pikir = message.text #4 Қадам пікір
		print(message.text)
		db = SQLight()
		db.update_kadam_4(123, kadam_4_pikir)
		bot.send_message(message.from_user.id, "<a href='https://www.youtube.com/watch?v=xIDxWY_7nfc'>5 Қадам</a>",parse_mode = "HTML")
		bot.send_message(message.from_user.id, "<b>Келесі қадамға өту үшін, пікір қалдырыңыз</b>"+u"\U0001F447", parse_mode = "HTML") #, reply_markup=ia_menu())
		dbworker.set_state(message.chat.id, config.States.kadam_5_pikir.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.kadam_5_pikir.value)
def kadam_5_pikir(message):
	if check_message(message.text,message):
		kadam_5_pikir = message.text #5 Қадам пікір
		print(message.text)
		db = SQLight()
		db.update_kadam_5(123, kadam_5_pikir)

		bot.send_message(message.from_user.id, "<a href='https://www.youtube.com/watch?v=D8wW7ycIHBE'>Қорытынды</a>",parse_mode = "HTML",reply_markup=zhukteu_batyrma())
		dbworker.set_state(message.chat.id, config.States.korytyndy.value)

@bot.callback_query_handler(func=lambda call: call.data == 'tandau_shenberi')
def sala_tandau_shenberi(call):
	bot.answer_callback_query(call.id, text="Күте тұрыңыз...")
	bot.send_message(call.from_user.id,'<a href="http://telegra.ph/file/d363e5bf0d48e565b1691.jpg">&#8203;</a>\U0001F391',parse_mode="HTML")
	bot.send_message(call.from_user.id,'<a href="https://youtu.be/YKIZetOkRFY">&#8203;</a>\U0001F3A5',parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == 'attyn_tort_aiyagy')
def sala_tandau_shenberi(call):
	bot.answer_callback_query(call.id, text="Күте тұрыңыз...")
	bot.send_message(call.from_user.id,'<a href="http://telegra.ph/file/b943663212c8930efcc3d.jpg">&#8203;</a>\U0001F391',parse_mode="HTML")
	bot.send_message(call.from_user.id,'<a href="https://youtu.be/d3b5LfZxWv8">&#8203;</a>\U0001F3A5',parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == 'tandau_tablicasy')
def sala_tandau_tablicasy(call):
	bot.answer_callback_query(call.id, text="Күте тұрыңыз...")
	bot.send_message(call.from_user.id,'Күте тұрыңыз, материалдар жүктелу үстінде...',parse_mode="HTML")
	bot.send_chat_action(call.from_user.id, 'upload_document')
	doc = open(constants.tandau_tablicasy, 'rb')
	bot.send_document(call.from_user.id, doc)
	#bot.send_message(call.from_user.id,'<a href="https://youtu.be/d3b5LfZxWv8">&#8203;</a>\U0001F3A5',parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == 'check_list')
def check_list(call):
	bot.answer_callback_query(call.id, text="Күте тұрыңыз...")
	bot.send_message(call.from_user.id,'Күте тұрыңыз, материалдар жүктелу үстінде...',parse_mode="HTML")
	bot.send_chat_action(call.from_user.id, 'upload_document')
	doc = open(constants.check_list, 'rb')
	bot.send_document(call.from_user.id, doc)

@bot.callback_query_handler(func=lambda call: call.data == 'tandau_prezentaciasy')
def tandau_prezentaciasy(call):
	bot.answer_callback_query(call.id, text="Күте тұрыңыз...")
	bot.send_message(call.from_user.id,'Күте тұрыңыз, материалдар жүктелу үстінде...',parse_mode="HTML")
	bot.send_chat_action(call.from_user.id, 'upload_document')
	doc = open(constants.tandau_prezentaciasy, 'rb')
	bot.send_document(call.from_user.id, doc)

@bot.callback_query_handler(func=lambda call: call.data == 'tandau_teoriasy')
def tandau_prezentaciasy(call):
	bot.answer_callback_query(call.id, text="Күте тұрыңыз...")
	bot.send_message(call.from_user.id,'Күте тұрыңыз, материалдар жүктелу үстінде...',parse_mode="HTML")
	bot.send_chat_action(call.from_user.id, 'upload_document')
	doc = open(constants.tandau_teoriasy, 'rb')
	bot.send_document(call.from_user.id, doc)


@bot.callback_query_handler(func=lambda call: call.data[:7] == 'zhukteu')
def zhukteu(call):
	bot.answer_callback_query(call.id, text="Күте тұрыңыз...")
	text = call.data[7:]
	if text == 'Material':
		markup = telebot.types.InlineKeyboardMarkup()
		row_0 = [telebot.types.InlineKeyboardButton(text="Аттың төрт аяғы", callback_data="attyn_tort_aiyagy")] #url na pdf
		row_1 = [telebot.types.InlineKeyboardButton(text="Сала таңдау шеңбері", callback_data="tandau_shenberi")] #url + url
		row_2 = [telebot.types.InlineKeyboardButton(text="Сала таңдау таблицасы", callback_data="tandau_tablicasy")]#url="https://drive.google.com/file/d/183M8k1QsRa230A5vldEW-KWkOzztOcPQ/view?usp=sharing")]
		row_3 = [telebot.types.InlineKeyboardButton(text="Чек лист", callback_data="check_list")]
		row_4 = [telebot.types.InlineKeyboardButton(text="Сала таңдау презентациясы", callback_data="tandau_prezentaciasy")] #url na tablicu
		row_5 = [telebot.types.InlineKeyboardButton(text="Сала таңдау теориясы", callback_data="tandau_teoriasy")] #url + url
		row_6 = [telebot.types.InlineKeyboardButton(text="Ресейдегі жолға қойылған кәсіптер", url="https://drive.google.com/open?id=1IwJtlRUrhJ7_iGirYCDo21NOPJRUS5Sf")]
		row_7 = [telebot.types.InlineKeyboardButton(text="Талқылар", callback_data="zhukteutalkylar")]
		row_8 = [telebot.types.InlineKeyboardButton(text="БМ кейстар", url="https://drive.google.com/drive/folders/1JaGXEU8Ki-ELb4Yr8qQgSNvgwZxmdqrY?usp=sharing")]
		row_9 = [telebot.types.InlineKeyboardButton(text="Эксперт топ", callback_data="zhukteuexpert")]
		
		markup.row(*row_0)
		markup.row(*row_1)
		markup.row(*row_2)
		markup.row(*row_3)
		markup.row(*row_4)
		markup.row(*row_5)
		markup.row(*row_6)
		markup.row(*row_7)
		markup.row(*row_8)
		markup.row(*row_9)
		bot.send_message(call.from_user.id, 'Ақпараттар...', reply_markup = markup)
		#return
	if text == 'expert':
		markup = telebot.types.InlineKeyboardMarkup()
		row_1 = [telebot.types.InlineKeyboardButton(text="ALMATY-EXPERT", url="https://t.me/almatyexpert")]
		row_2 = [telebot.types.InlineKeyboardButton(text="shopikon", url="http://shopikonbb.kz/")]
		row_3 = [telebot.types.InlineKeyboardButton(text="InterSell.kz", url="https://intersell.kz/")]
		
		markup.row(*row_1)
		markup.row(*row_2)
		markup.row(*row_3)

		bot.send_message(call.from_user.id, 'Эксперт топтар...', reply_markup = markup)

	if text == 'Video':
		markup = telebot.types.InlineKeyboardMarkup()
		row_1 = [telebot.types.InlineKeyboardButton(text="Ондығымды тыңдап жотама жеттім", url="https://www.youtube.com/watch?v=ml2GABW8EdY")]
		row_2 = [telebot.types.InlineKeyboardButton(text="Шет елден жақсы товар тауып соны сата бастадым", url="https://www.youtube.com/watch?v=LcBsJy1Vd8c")]
		row_3 = [telebot.types.InlineKeyboardButton(text="Хоббиімді салаға айналдырып, 2 300 000 таптым", url="https://www.youtube.com/watch?v=-5gMwQOzMzM")]
		row_4 = [telebot.types.InlineKeyboardButton(text="Көрші елдегі саланы Қазақстанға алып келіп, жетістікке жеттім", url="https://www.youtube.com/watch?v=dU6P7-jzdeA")]
		row_5 = [telebot.types.InlineKeyboardButton(text="7 құралды игеру мақсатында сауданы таңдадым!", url="https://www.youtube.com/watch?v=-Z_j3ejA_bE")]
		row_6 = [telebot.types.InlineKeyboardButton(text="Тренердің талқысынан кейін, саламды таптым", url="https://www.youtube.com/watch?v=cRrK_YNxp68")]
		row_7 = [telebot.types.InlineKeyboardButton(text="Достарыммен серіктес болып, өзімді таптым (жетістікке жеттім)", url="https://www.youtube.com/watch?v=zRnCSH-drEc")]
		row_8 = [telebot.types.InlineKeyboardButton(text="Астанадан келіп, армандаған салама қол жеткіздім", url="https://www.youtube.com/watch?v=36QFz628SWU")]
		row_9 = [telebot.types.InlineKeyboardButton(text="Тауарларды тестілеу арқылы 2000 000 жетістікке жеттім", url="https://www.youtube.com/watch?v=KMs8Mn-xAjw")]
		row_10 = [telebot.types.InlineKeyboardButton(text="2 ай уақытты бос өткізбейін деп, сауданы таңдадым", url="https://www.youtube.com/watch?v=rKZiCwadG4Q")]
		row_11 = [telebot.types.InlineKeyboardButton(text="Проблемамды міндетіме айналдырып, жетістікке жеттім", url="https://www.youtube.com/watch?v=FjmQ0suiOyo")]
		row_12 = [telebot.types.InlineKeyboardButton(text="Онбасылардың талқысына күмәнмен қарап, бірақ саламды таптым", url="https://www.youtube.com/watch?v=YoaDgaqywnE")]
		row_13 = [telebot.types.InlineKeyboardButton(text="Ішіме үңіліп, қабілетімді салама айналдырдым", url="https://www.youtube.com/watch?v=1QyccWKMzO8")]
		row_14 = [telebot.types.InlineKeyboardButton(text='"Кради как художник"- деп, өндіріспен айналысып кеттім.', url="https://www.youtube.com/watch?v=DrASklxuW74")]
		row_15 = [telebot.types.InlineKeyboardButton(text="Бірге бір жасағасын динозавр таптым", url="https://www.youtube.com/watch?v=XPztB4XmVEs")]
		row_kelesi_kadam = [telebot.types.InlineKeyboardButton(text="Келесі қадамға өту", callback_data = 'kadam_3')]

		markup.row(*row_1)
		markup.row(*row_2)
		markup.row(*row_3)
		markup.row(*row_4)
		markup.row(*row_5)
		markup.row(*row_6)
		markup.row(*row_7)
		markup.row(*row_8)
		markup.row(*row_9)
		markup.row(*row_10)
		markup.row(*row_11)
		markup.row(*row_12)
		markup.row(*row_13)
		markup.row(*row_14)
		markup.row(*row_15)

		markup.row(*row_kelesi_kadam)
		bot.send_message(call.from_user.id, 'Кейстар...', reply_markup = markup)

	if text == 'talkylar':
		markup = telebot.types.InlineKeyboardMarkup()
		row_1 = [telebot.types.InlineKeyboardButton(text="Құрылыс және аяқ киім саудасы", url="https://youtu.be/MbugCojYJUM")]
		row_2 = [telebot.types.InlineKeyboardButton(text="Динозаврмен жұмыс. Сатылымды өсіру", url="https://youtu.be/H0CFjpIN4uA")]
		row_3 = [telebot.types.InlineKeyboardButton(text="Балалар киімін сату", url="https://youtu.be/8gCelUt7V-U")]
		row_4 = [telebot.types.InlineKeyboardButton(text="Бейне бақылауды орнату", url="https://youtu.be/oF763DWjzhM")]
		row_5 = [telebot.types.InlineKeyboardButton(text="Торт жасап үйретуге мастер класс өткізу", url="https://youtu.be/UjVgc2cWp1o")]
		row_6 = [telebot.types.InlineKeyboardButton(text="Аяқ киім өндірісі", url="https://youtu.be/2ktUwNgEEUc")]
		row_7 = [telebot.types.InlineKeyboardButton(text="Грунтовка өндірісі", url="https://youtu.be/IN1o12AuC_8")]
		row_8 = [telebot.types.InlineKeyboardButton(text="ҰБТ-ға дайындау қызметі", url="https://youtu.be/oKH5msFaqG0")]
		row_9 = [telebot.types.InlineKeyboardButton(text="Кірпік өсіру қызметі", url="https://youtu.be/mrQQraakJuE")]
		row_10 = [telebot.types.InlineKeyboardButton(text="Француз тілінде оқыту қызметі", url="https://youtu.be/4XzfPBg7jnc")]
		row_11 = [telebot.types.InlineKeyboardButton(text="Массаж қызметі", url="https://youtu.be/3rG3lz-XT4o")]
		row_12 = [telebot.types.InlineKeyboardButton(text="Риэлтор қызметі", url="https://youtu.be/604ul_B4Z2w")]
		row_13 = [telebot.types.InlineKeyboardButton(text="Кейтеринг қызметі", url="https://youtu.be/F5NlHovItxQ")]
		row_14 = [telebot.types.InlineKeyboardButton(text='3 саланының талқысы', url="https://youtu.be/MW9_2a8BwF8")]
		row_15 = [telebot.types.InlineKeyboardButton(text="Массаж қызметінің талқысы", url="https://youtu.be/LGyDmLElGew")]
		
		row_16 = [telebot.types.InlineKeyboardButton(text="Ауылда Қолөнермен айналысамын", url="https://youtu.be/YaoWEAsOVaw")]
		row_17 = [telebot.types.InlineKeyboardButton(text="Терминал орнату", url="https://youtu.be/jJtUxO2qL8Y")]
		row_18 = [telebot.types.InlineKeyboardButton(text="Егінді қойып Мал бағамын", url="https://youtu.be/8f-jgCEXZTg")]
		row_19 = [telebot.types.InlineKeyboardButton(text="Жихаз саласымен екі айда 600 000 тг табамын", url="https://youtu.be/F1AsJO3Snp4")]
		row_20 = [telebot.types.InlineKeyboardButton(text="Шино переработка", url="https://youtu.be/oXBGFvCx-B8")]
		row_21 = [telebot.types.InlineKeyboardButton(text="2 айда Ата-анаңа жақсылық жаса", url="https://youtu.be/G5ALKo6K0V0")]
		row_22 = [telebot.types.InlineKeyboardButton(text="Астау сату. Динозавр тауып, алға жылжыту", url="https://youtu.be/hX-l9jqhSS8")]
		row_23 = [telebot.types.InlineKeyboardButton(text="Татуажбен акша жинап, туристік фирма ашу", url="https://youtu.be/zz-ZdoGmWj8")]
		row_24 = [telebot.types.InlineKeyboardButton(text="Динозаврмен жұмыс. Сатылымды өсіру", url="https://youtu.be/H0CFjpIN4uA")]
		row_25 = [telebot.types.InlineKeyboardButton(text="Балалар киімін сату", url="https://youtu.be/8gCelUt7V-U")]
		row_26 = [telebot.types.InlineKeyboardButton(text="Бейне бақылауды орнату", url="https://youtu.be/oF763DWjzhM")]
		row_27 = [telebot.types.InlineKeyboardButton(text="Торт жасап үйретуге мастер класс өткізу", url="https://youtu.be/UjVgc2cWp1o")]
		row_28 = [telebot.types.InlineKeyboardButton(text="Кейтеринг қызметі", url="https://youtu.be/F5NlHovItxQ")]
		row_29 = [telebot.types.InlineKeyboardButton(text='Аяқ киім өндірісі', url="https://youtu.be/2ktUwNgEEUc")]
		row_30 = [telebot.types.InlineKeyboardButton(text="Грунтовка өндірісі", url="https://youtu.be/IN1o12AuC_8")]
		row_31 = [telebot.types.InlineKeyboardButton(text="ҰБТ-ға дайындау қызметі", url="https://youtu.be/oKH5msFaqG0")]
		row_32 = [telebot.types.InlineKeyboardButton(text="Дубайлық бизнесмен | Кілеммен айналысып бастадым", url="https://youtu.be/wuR-WiOqKgg")]
		row_33 = [telebot.types.InlineKeyboardButton(text="Құрылыс және аяқ киім саудасы", url="https://youtu.be/MbugCojYJUM")]
		
		markup.row(*row_1)
		markup.row(*row_2)
		markup.row(*row_3)
		markup.row(*row_4)
		markup.row(*row_5)
		markup.row(*row_6)
		markup.row(*row_7)
		markup.row(*row_8)
		markup.row(*row_9)
		markup.row(*row_10)
		markup.row(*row_11)
		markup.row(*row_12)
		markup.row(*row_13)
		markup.row(*row_14)
		markup.row(*row_15)

		markup.row(*row_16)
		markup.row(*row_17)
		markup.row(*row_18)
		markup.row(*row_19)
		markup.row(*row_20)
		markup.row(*row_21)
		markup.row(*row_22)
		markup.row(*row_23)
		markup.row(*row_24)
		markup.row(*row_25)
		markup.row(*row_26)
		markup.row(*row_27)
		markup.row(*row_28)
		markup.row(*row_29)
		markup.row(*row_30)
		markup.row(*row_31)
		markup.row(*row_32)
		markup.row(*row_33)
		bot.send_message(call.from_user.id, '<b>Талқылар...</b>',parse_mode = 'HTML', reply_markup = markup)


@bot.message_handler(content_types=['text'])
def text_message(message):
	if message.text == 'excel':
		db = SQLight()
		db.get_excel(message.from_user.id)
		return
bot.remove_webhook()
bot.polling(True)
