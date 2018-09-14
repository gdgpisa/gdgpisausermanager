# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import time
import os
import random
import threading

TOKEN = ""
expire = 0
chat = ""
uid = ""
mexid = ""

def welcome(bot, update):
    for new_user_obj in update.message.new_chat_members:
	global expire
	expire = 0
	new_user = ""
        try:
            new_user = "@" + new_user_obj['username']
        except Exception as e:
            new_user = new_user_obj['first_name'];
	print("Nuovo utente: "+new_user)
	global chat
	global uid
	global mexid
	chat = update.message.chat_id
	uid = new_user_obj
	keyboard = [[InlineKeyboardButton("Confermo", callback_data=1)]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	mexid = bot.send_message(chat, text="Benvenut* " + str(new_user) + "! Premi 'Confermo' per dimostrare di non essere un bot.", reply_markup=reply_markup)
	#threading.Timer(30.0, timer, [bot, update]).start()
	return

def button_pressed(bot, update, user_data):
	global expire
	global chat
	global mexid
	global uid
	user = update.message.from_user
	print(Prima)
	print(user_data)
	print(uid["username"])
	if(user_data == uid["username"]):
		expire = 1
		print("Registrazione completata")
		bot.deleteMessage(chat, mexid['message_id'])
		bot.send_message(chat, text= str(new_user) + ", grazie per aver completato la registrazione!")
	else:
		print("Utente errato!")
		
def main():
	updater = Updater(TOKEN)
	dp = updater.dispatcher
	dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
	dp.add_handler(CallbackQueryHandler(button_pressed, pass_user_data=True))
	updater.start_polling()
	updater.idle()

def timer(bot, update):
	global uid
	global expire
	global chat
	global mexid
	if expire != 1:
		print("Kick")
		bot.kickChatMember(chat, uid["id"], until_date=25)
		bot.deleteMessage(chat, mexid['message_id'])
	return 
		

try:
	if __name__ == '__main__':
		main()
except KeyboardInterrupt:
	print ("Chiusura programma")
