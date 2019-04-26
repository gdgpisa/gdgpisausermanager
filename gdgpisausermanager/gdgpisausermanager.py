# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import threading
from sys import maxsize

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ParseMode
from telegram.error import NetworkError, BadRequest
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from gdgpisausermanager.config import Config


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
    for new_user_obj in update.message.new_chat_members:  # new_user_obj has telegram.user.User type
        user_handle = new_user_obj.name
        user_id = new_user_obj.id
        chat_id = update.message.chat_id

        if (user_id == bot.id):
            bot.send_message(
                chat_id = update.message.chat_id,
                text = "🤖 Hi folks!\nI'll kick out all the fake users that don't press my button.\nKeep chat and do not spam! 🤟\n\nRemember to promote me to administrator.")
            return
        
        reply_text = "Welcome " + user_handle + "! Press <i>Confirm</i> to prove you are not a bot."

        new_users.append(new_user_obj.id)

        keyboard = [[InlineKeyboardButton("Confirm", callback_data=1)]]
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
            args=[bot, user_id, chat_id, message.message_id],
        ).start()

        logger.debug("New user: " + user_handle)


def button_pressed(bot, update):
    """
    :type bot: telegram.Bot
    :type update: telegram.Update
    """
    if update.callback_query.from_user.id in new_users:
        user_handle = update.callback_query.from_user.name
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id

        new_users.remove(update.callback_query.from_user.id)
        bot.delete_message(chat_id, message_id=message_id)

        bot.send_message(
            chat_id,
            text = "Please welcome " + user_handle + "! 🎉\nThank you for completing the captcha."
        )

        logger.debug("Confirmed user: " + user_handle)


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
    try:
        return any(user_id == admin.user.id for admin in bot.get_chat_administrators(chat_id))
    except NetworkError:
        return False


def ban_user(bot, update):
    """
    :type bot: telegram.Bot
    :type update: telegram.Update
    """
    if update.message.reply_to_message is None:
        return

    chat_id = update.message.chat.id

    if is_admin(bot, user_id=update.message.from_user.id, chat_id=chat_id):
        user_id = update.message.reply_to_message.from_user.id
        user_handle = update.message.reply_to_message.from_user.name

        if not is_admin(bot, user_id, chat_id):
            bot.kick_chat_member(chat_id, user_id)
            bot.send_message(
                chat_id,
                text = user_handle + "banned."
            )

            logger.info("Banned user: " + user_handle)


def kick_user(bot, update):
    """
    :type bot: telegram.Bot
    :type update: telegram.Update
    """
    if update.message.reply_to_message is None:
        return

    chat_id = update.message.chat.id

    if is_admin(bot, user_id=update.message.from_user.id, chat_id=chat_id):
        user_id = update.message.reply_to_message.from_user.id
        user_handle = update.message.reply_to_message.from_user.name

        if is_admin(bot, user_id, chat_id):
            bot.kick_chat_member(chat_id, user_id)
            bot.unban_chat_member(chat_id, user_id)

            logger.info("The user {} was kicked with success.".format(user_handle))


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
        print("KeyboardInterrupt: shutting down the bot...")


def timer(bot, user_id, chat_id, message_id):
    """
    :type bot: telegram.Bot
    :type user_id: str or int
    :type chat_id: str or int
    :type message_id: str or int
    """
    if user_id in new_users:
        logger.info("User with id: {} auto-removed with success".format(user_id))
        new_users.remove(user_id)
        try:
            bot.kick_chat_member(chat_id, user_id, until_date=maxsize)  # Kicking a member for over 365 days is forever
            bot.delete_message(chat_id, message_id=message_id)
        except BadRequest:
            bot.send_message(
                chat_id,
                text = "You need to promote me as an administrator to kick out users. I need permissions to ban users and delete messages."
            )


if __name__ == '__main__':
    exit(main())
