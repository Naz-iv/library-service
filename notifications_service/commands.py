# from core.settings import CHAT_ID
# from borrowing_service.signals import notify_new_borrowing


def welcome_message(bot, message) -> None:
    name = ""

    if message.from_user.last_name is None:
        name = f"{message.from_user.first_name}"
    else:
        name = f"{message.from_user.full_name}"

    bot.reply_to(message,
                 f"Hello, {name}!\n"
                 f"Welcome to the Library Service!\n\n"
                 f"/help for more information")


def help_information(bot, message) -> None:
    bot.reply_to(message,
                 "/start - start bot\n"
                 "/help - show information about commands\n"
                 "/my_borrowings - show all your borrowings\n")


# @shared_task
# def user_borrowings(bot, message) -> None:
#     user_id = message.from_user.id
#     borrowings_info = notify_new_borrowing(user_id)
#     bot.reply_to(message, f"""
#     your borrs: \n
#     {borrowings_info}
#     """)
