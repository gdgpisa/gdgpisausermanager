# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from config import Config
import datetime
import time
import os
import random
import threading
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

new_users = []


def welcome(bot, update):
    for new_user_obj in update.message.new_chat_members:
        try:
            new_user = "@" + new_user_obj['username']
            reply_text = "Benvenut* <a href=\"t.me/{}\">{}</a> in <b>{}</b>! Premi <i>Confermo</i> per dimostrare di non essere un bot." \
                .format(new_user_obj.username, new_user, update.message.chat.title)
        except Exception as _:
            new_user = new_user_obj['first_name']
            reply_text = "Benvenut* {} in <b>{}</b>! Premi <i>Confermo</i> per dimostrare di non essere un bot." \
                .format(new_user, update.message.chat.title)
        logger.info("Nuovo utente: {}".format(new_user))

        new_users.append(new_user_obj.id)

        keyboard = [[InlineKeyboardButton("Confermo", callback_data=1)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        mexid = bot.send_message(
            update.message.chat_id,
            text=reply_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

        threading.Timer(Config.WAITING_TIMEOUT, timer,
                        [bot, new_user_obj.id, update.message.chat_id, mexid.message_id]).start()
        return


def button_pressed(bot, update):
    if update.callback_query.from_user.id in new_users:
        new_users.remove(update.callback_query.from_user.id)
        bot.deleteMessage(update.callback_query.message.chat_id, update.callback_query.from_user.id)

        try:
            user = "@" + update.callback_query.from_user.username
        except Exception as _:
            user = update.callback_query.from_user.first_name

        bot.send_message(update.callback_query.message.chat_id,
                         text=str(user) + ", grazie per aver completato la registrazione!")


def check_activity(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="pong",
        reply_to_message_id=update.message.message_id)


def is_admin(bot, userid, chatid):
    return userid in [admin.user.id for admin in bot.get_chat_administrators(chatid)]


def ban_user(bot, update):
    if update.message.reply_to_message is None:
        return

    if is_admin(bot, update.message.from_user.id, update.message.chat.id):
        if not is_admin(bot, update.message.reply_to_message.from_user.id, update.message.chat.id):
            reply_text = "{} è stato bannato con successo.".format(update.message.reply_to_message.from_user.username)
            bot.kickChatMember(update.message.chat.id, update.message.reply_to_message.from_user.id)
            bot.send_message(update.message.chat.id, text=reply_text)

            try:
                user = "@" + update.message.reply_to_message.from_user.username
            except Exception as _:
                user = update.message.reply_to_message.from_user.first_name

            logger.info("The user {} was banned with success".format(user))


def kick_user(bot, update):
    if update.message.reply_to_message is None:
        return

    if is_admin(bot, update.message.from_user.id, update.message.chat.id):
        if not is_admin(bot, update.message.reply_to_message.from_user.id, update.message.chat.id):
            bot.kickChatMember(update.message.chat.id, update.message.reply_to_message.from_user.id)
            bot.unbanChatMember(update.message.chat.id, update.message.reply_to_message.from_user.id)

            try:
                user = "@" + update.message.reply_to_message.from_user.username
            except Exception as _:
                user = update.message.reply_to_message.from_user.first_name

            logger.info("The user {} was kicked with success".format(user))


def main():
    updater = Updater(Config.TOKEN)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.regex('^ping$'), check_activity))
    dp.add_handler(CallbackQueryHandler(button_pressed))
    dp.add_handler(CommandHandler('ban', ban_user))
    dp.add_handler(CommandHandler('kick', kick_user))

    updater.start_polling()
    updater.idle()


def timer(bot, userid, chatid, mexid):
    global new_users
    if userid in new_users:
        logger.info("User with id: {} auto-removed with success".format(userid))
        bot.kickChatMember(chatid, userid, until_date=25)
        bot.deleteMessage(chatid, mexid)
    return


try:
    if __name__ == '__main__':
        main()
except KeyboardInterrupt:
    print("Chiusura programma")
