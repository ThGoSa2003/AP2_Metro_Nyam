from restaurants import *
from city import *
import python-telegram-bot
from telegram.ext import Updater, CommandHandler

class Bot:
    current_position: Coord
    city_graph: CityGraph

    def __init__(self, current_position: Coord):
        self.current_position = (0,0)
        city_graph = load_city_graph("graph", "city_graph")

    def start(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hola! Soc un bot per trobar la ruta més ràpida al restaurant que vulguis de Barcelona. \
                    Abans de res escriu-me la posició on et trobes.")
        

    def help(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Les comandes que pots utilitzar són les següents:")

    def author(self, update, context):
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
