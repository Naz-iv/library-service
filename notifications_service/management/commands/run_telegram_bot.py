import telebot
from django.core.management import BaseCommand

from core.settings import CHAT_ID, TELEGRAM_BOT_TOKEN
from notifications_service.bot_commands import (welcome_message,
                                                help_information,
                                                user_borrowings,
                                                is_user)


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

        def start_telegram_bot():
            bot.polling()

        @bot.message_handler(commands=["start"])
        def login(message):
            if not is_user(message):
                bot.send_message(message.chat.id,
                                 text="Enter your email to login: ")
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

        def send_telegram_notification(message):
            bot.send_message(CHAT_ID, text=message)

        start_telegram_bot()
