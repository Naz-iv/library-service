import telebot
from django.core.management import BaseCommand

from core.settings import CHAT_ID, TELEGRAM_BOT_TOKEN
from notifications_service.commands import welcome_message, help_information
# from django_q.tasks import async_task


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

        def start_telegram_bot():
            bot.polling()

        @bot.message_handler(commands=["start"])
        def send_welcome(message) -> None:
            welcome_message(bot, message)

        @bot.message_handler(commands=["help"])
        def send_help_information(message: telebot.types.Message) -> None:
            help_information(bot, message)

        # @bot.message_handler(commands=["my_borrowings"])
        # def send_users_borrowings(message: telebot.types.Message) -> None:
        #     async_task(user_borrowings, bot, message)

        def send_telegram_notification(message):
            bot.send_message(CHAT_ID, text=message)

        start_telegram_bot()
