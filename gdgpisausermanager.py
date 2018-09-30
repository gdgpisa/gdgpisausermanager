# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import threading

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ParseMode
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from config import Config


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

new_users = []


def welcome(bot, update):
    """
    :type bot: telegram.Bot
    :type update: telegram.Update
    """
    for new_user_obj in update.message.new_chat_members:
        try:
            new_user = "@{}".format(new_user_obj['username'])
            # TODO: is format really needed?
            reply_text = "Benvenut*"+new_user+"! Premi <i>Confermo</i> per dimostrare di non essere un bot." \
                .format(new_user_obj.username, new_user, update.message.chat.title)
        except Exception as _:
            new_user = "@{}".format(new_user_obj['first_name'])
            # TODO: is format really needed?
            reply_text = "Benvenut*"+new_user+"! Premi <i>Confermo</i> per dimostrare di non essere un bot." \
                .format(new_user, update.message.chat.title)

        new_users.append(new_user_obj.id)

        keyboard = [[InlineKeyboardButton("Confermo", callback_data=1)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message = bot.send_message(
            chat_id=update.message.chat_id,
            text=reply_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
        )

        threading.Timer(
            interval=Config.WAITING_TIMEOUT,
            function=timer,
            args=[bot, new_user_obj.id, update.message.chat_id, message.message_id],
        ).start()

        logger.info("Nuovo utente: {}.".format(new_user))


def button_pressed(bot, update):
    """
    :type bot: telegram.Bot
    :type update: telegram.Update
    """
    global new_users

    if update.callback_query.from_user.id in new_users:

        new_users.remove(update.callback_query.from_user.id)
        bot.delete_message(update.callback_query.message.chat_id, update.callback_query.message.message_id)

        try:
            user = "@{}".format(update.callback_query.from_user.username)
        except Exception as _:
            user = update.callback_query.from_user.first_name

        bot.send_message(
            chat_id=update.callback_query.message.chat_id,
            text="{user}, grazie per aver completato la registrazione!".format(user=user),
        )

        logger.info("Utente confermato: {}.".format(user))


def check_activity(bot, update):
    """
    :type bot: telegram.Bot
    :type update: telegram.Update
    """
    bot.send_message(
        chat_id=update.message.chat_id,
        text="pong",
        reply_to_message_id=update.message.message_id,
    )


def is_admin(bot, user_id, chat_id):
    """
    :type bot: telegram.Bot
    :type user_id: str or int
    :type chat_id: str or int
    """
    return any(user_id == admin.user.id for admin in bot.get_chat_administrators(chat_id))


def ban_user(bot, update):
    """
    :type bot: telegram.Bot
    :type update: telegram.Update
    """
    if update.message.reply_to_message is None:
        return

    if is_admin(bot, update.message.from_user.id, update.message.chat.id):
        if not is_admin(bot, update.message.reply_to_message.from_user.id, update.message.chat.id):
            reply_text = "{} è stato bannato con successo.".format(update.message.reply_to_message.from_user.username)
            bot.kick_chat_member(update.message.chat.id, update.message.reply_to_message.from_user.id)
            bot.send_message(update.message.chat.id, text=reply_text)

            try:
                user = "@{}".format(update.message.reply_to_message.from_user.username)
            except Exception as _:
                user = update.message.reply_to_message.from_user.first_name

            logger.info("The user {} was banned with success".format(user))


def kick_user(bot, update):
    """
    :type bot: telegram.Bot
    :type update: telegram.Update
    """
    if update.message.reply_to_message is None:
        return

    if is_admin(bot, update.message.from_user.id, update.message.chat.id):
        if not is_admin(bot, update.message.reply_to_message.from_user.id, update.message.chat.id):
            bot.kick_chat_member(update.message.chat.id, update.message.reply_to_message.from_user.id)
            bot.unban_chat_member(update.message.chat.id, update.message.reply_to_message.from_user.id)

            try:
                user = "@{}".format(update.message.reply_to_message.from_user.username)
            except Exception as _:
                user = update.message.reply_to_message.from_user.first_name

            logger.info("The user {} was kicked with success".format(user))


def main():
    updater = Updater(Config.TOKEN)
    updater.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^ping$'), check_activity))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_pressed))
    updater.dispatcher.add_handler(CommandHandler('ban', ban_user))
    updater.dispatcher.add_handler(CommandHandler('kick', kick_user))

    updater.start_polling()

    try:
        updater.idle()
    except KeyboardInterrupt:
        print("Chiusura programma")


def timer(bot, user_id, chat_id, message_id):
    """
    :type bot: telegram.Bot
    :type user_id: str or int
    :type chat_id: str or int
    :type message_id: str or int
    """
    global new_users
    if user_id in new_users:
        logger.info("User with id: {} auto-removed with success".format(user_id))
        bot.kick_chat_member(chat_id=chat_id, user_id=user_id, until_date=25)
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    return


if __name__ == '__main__':
    exit(main())
