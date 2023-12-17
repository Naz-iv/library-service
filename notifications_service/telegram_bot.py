import telebot
# from borrowing_service.models import Borrowing
# from borrowing_service.signals import notify_all_borrowings
from core.settings import TELEGRAM_BOT_TOKEN, CHAT_ID


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message) -> None:
    name = ""

    if message.from_user.last_name is None:
        name = f"{message.from_user.first_name}"
    else:
        name = f"{message.from_user.full_name}"

    bot.reply_to(message,
                 f"Hello, {name}!\n"
                 f"Welcome to the Library Service!\n\n"
                 f"/help for more information")


@bot.message_handler(commands=["help"])
def send_help_information(message: telebot.types.Message) -> None:
    bot.reply_to(message,
                 "/start - start bot\n"
                 "/help - show information about commands\n"
                 "/my_borrowings - show all your borrowings\n")


# @bot.message_handler(commands=["my_borrowings"])
# def send_users_borrowings(message: telebot.types.Message) -> None:
#     user_id = message.from_user.id
#     borrowings_info = notify_all_borrowings(user_id)
#     bot.reply_to(message, f"""
#     your borrs: \n
#     {borrowings_info}
#     """)

def send_telegram_notification(message):
    bot.send_message(CHAT_ID, text=message)


bot.polling()
