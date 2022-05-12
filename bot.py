from restaurants import *
from city import *
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters



class Bot:
    city_graph: CityGraph
    all_restaurants: Restaurants
    restaurants_of_the_search: Restaurants

    def __init__(self):
        self.st_graph = load_osmnx_graph("graph")
        self.city_graph = load_city_graph("graph", "city_graph")
        self.all_restaurants = read()
        self.restaurants_of_the_search = []

    def start(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hola! Soc un bot per trobar la ruta més ràpida al restaurant que vulguis de Barcelona. \
                    Abans de res escriu-me la posició on et trobes.")

    def help(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Les comandes que pots utilitzar són les següents:\n\
                    /author: mostra el nom dels autors del programa.\n\
                    /find <query>: Cerca quins restaurants satisfan la cerca i n'escriu una \
                        llista numerada (12 elements com a molt). Per exemple: /find pizza. \n\
                    /info <numero>: mostra la informació sobre el restaurant especificat pel \
                        seu número (triat de la darrera llista numerada obtinguda amb /find).\n\
                    /guide <numero>: mostra un mapa amb el camí més curt per anar del punt \
                        actual on es troba l'usuari al restaurant especificat pel seu número \
                        (triat de la darrera llista numerada obtinguda amb /find).")

    def author(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Aquest programa està fet per Oriol López Petit i Thomas González Saito.")

    def find(self, update, context):
        query = str(context.args[0])
        self.restaurants_of_the_search = find(query, all_restaurants)
        for i in range(len(self.restaurants_of_the_search)):
            print(i, self.restaurants_of_the_search[i].name)

    def info(self, update, context):
        numero = int(context.args[0])
        print("Informació de", self.restaurants_of_the_search[numero])
        for attribute, value in vars(self.restaurants_of_the_search[numero]).items():
            print(attribute, value)

    def guide(self, update, context):
        numero = int(context.args[0])
        plot_path(self.city_graph, find_path(self.st_graph,
            self.city_graph, update.message.location,
            self.restaurants_of_the_search[numero].pos),
            "path")
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open("path.png", 'rb'))
        os.remove("path_bot.png")

"""
    def unknown(update, context):
        update.message.reply_text(
            "Sorry '%s' is not a valid command" % update.message.text)


    def unknown_text(update, context):
        update.message.reply_text(
            "Sorry I can't recognize you , you said '%s'" % update.message.text)
"""
def main():

    bot = Bot()
    updater = Updater("5321497109:AAGV1x85pE9xvVicVyihaNJV6FcdR2QTe1s", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', bot.start))
    dispatcher.add_handler(CommandHandler('help', bot.help))
    dispatcher.add_handler(CommandHandler('author', bot.author))
    dispatcher.add_handler(CommandHandler('find', bot.find))
    dispatcher.add_handler(CommandHandler('info', bot.info))
    dispatcher.add_handler(CommandHandler('guide', bot.guide))
    """
    dispatcher.add_handler(MessageHandler(Filters.text, unknown))
    dispatcher.add_handler(MessageHandler(
    command, unknown))  # Filters out unknown commands

    # Filters out unknown messages.
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
    """
    updater.start_polling()

if __name__ == "__main__":
    main()
