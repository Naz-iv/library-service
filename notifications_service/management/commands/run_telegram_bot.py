import telebot
from django.core.management import BaseCommand

from core.settings import TELEGRAM_BOT_TOKEN
from notifications_service.bot_commands import (
    welcome_message,
    help_information,
    user_borrowings,
    is_user
)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def login(message):
    if not is_user(message):
        bot.send_message(message.chat.id, text="Enter your email to login ")
        bot.register_next_step_handler(message, login)
    else:
        authorised(message)


def authorised(message):
    welcome_message(bot, message)


@bot.message_handler(commands=["help"])
def send_help_information(message: telebot.types.Message) -> None:
    help_information(bot, message)


@bot.message_handler(commands=["my_borrowings"])
def send_users_borrowings(message: telebot.types.Message) -> None:
    user_borrowings(bot, message)


def send_notification(chat_id, message):
    bot.send_message(chat_id, message)


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot.polling()
