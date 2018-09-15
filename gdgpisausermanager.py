# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup 
import datetime
import time
import os
import random
import threading

TOKEN = ""
new_users = []
WAITING_TIMEOUT = 30.0

def welcome(bot, update):
	for new_user_obj in update.message.new_chat_members:
		print(update.message.chat.title)

		try:
			new_user = "@" + new_user_obj['username']
		except Exception as e:
			new_user = new_user_obj['first_name']
		print("Nuovo utente: "+new_user)
		reply_text = "Benvenut* {} in *{}*! Premi _Confermo_ per dimostrare di non essere un bot.".format(str(new_user), str(update.message.chat.title))

		new_users.append(new_user_obj.id)

		keyboard = [[InlineKeyboardButton("Confermo", callback_data=1)]]
		reply_markup = InlineKeyboardMarkup(keyboard)

		mexid = bot.send_message(
			update.message.chat_id,
			text=reply_text,
			reply_markup=reply_markup
			)

		threading.Timer(WAITING_TIMEOUT, timer, [bot, new_user_obj.id, update.message.chat_id, mexid.message_id]).start()
		return

def button_pressed(bot, update):
	if update.callback_query.from_user.id in new_users:
		new_users.remove(update.callback_query.from_user.id) 
		bot.deleteMessage(update.callback_query.message.chat_id, update.callback_query.from_user.id)

		try:
			user = "@" + update.callback_query.from_user.username
		except Exception as e:
			user = update.callback_query.from_user.first_name
		
		bot.send_message(update.callback_query.message.chat_id, text= str(user) + ", grazie per aver completato la registrazione!")
	else:
		print("Utente errato!")

def check_activity(bot, update):
	bot.send_message(
		chat_id=update.message.chat_id,
		text="pong",
		reply_to_message_id=update.message.message_id)
		
def main():
	updater = Updater(TOKEN)
	dp = updater.dispatcher
	dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
	dp.add_handler(MessageHandler(Filters.regex('^ping$'), check_activity))
	dp.add_handler(CallbackQueryHandler(button_pressed))
	updater.start_polling()
	updater.idle()

def timer(bot, userid, chatid, mexid):
	global new_users
	if userid in new_users:
		print("Kick")
		bot.kickChatMember(chatid, userid, until_date=25)
		bot.deleteMessage(chatid, mexid)
	return

try:
	if __name__ == '__main__':
		main()
except KeyboardInterrupt:
	print ("Chiusura programma")
