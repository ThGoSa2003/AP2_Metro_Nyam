from restaurants import *
from city import *
from telegram.ext import Updater, CommandHandler

class Bot:
    current_position: Coord
    city_graph: CityGraph
    all_restaurants: Restaurants
    restaurants_of_the_search: Restaurants

    def __init__(self):
        self.current_position = (0,0)
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
        plot_path(self.city_graph, find_path(st_graph, city_graph, self.current_position, self.restaurants_of_the_search[numero].pos), "path")

def main():

    bot = Bot()

    TOKEN = open('./token.txt', "w+").read().strip()
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
