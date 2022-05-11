from restaurants import *
from city import *
import python-telegram-bot
from telegram.ext import Updater, CommandHandler

class Bot:
    current_position: Coord
    city_graph: CityGraph


    def start(update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hola! Soc un bot per trobar la ruta més ")

    def help(update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hola! Soc un bot.")

    def author(update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Aquest programa està fet per Oriol López Petit i Thomas González Saito.")


def main():

    bot = Bot()

    TOKEN = open('token.txt').read().strip()
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', bot.start))
    dispatcher.add_handler(CommandHandler('help', bot.help))
    dispatcher.add_handler(CommandHandler('author', bot.author))
    dispatcher.add_handler(CommandHandler('find', bot.find))
    dispatcher.add_handler(CommandHandler('info', bot.info))
    dispatcher.add_handler(CommandHandler('guide', bot.guide))

    updater.start_polling()

if __name__ == "__main__":
    main()
