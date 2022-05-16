import restaurants
from city import St_node
import city
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters



class Bot:
    st_graph: city.OsmnxGraph
    city_graph: city.CityGraph
    restaurants: restaurants.Restaurants
    coord = list[int,int] # (latitude, longitude)


    def __init__(self) -> None:
        self.st_graph = city.load_osmnx_graph("graph.gpickle")
        self.city_graph = city.load_city_graph("graph.gpickle", "city_graph.gpickle")
        self.restaurants = restaurants.read()
        self.coord = [0,0]

    def help(self, update, context) -> None:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = " Per obtenir els resultats més acurats sobre les rutes que tens que navegar agafem la teva geolocalització de forma automatica, pero si vols la pots actualitzar amb la comanda /locationLes comandes que pots utilitzar són les següents:\n\
        /author: mostra el nom dels autors del programa.\n\
        /find <query>: Cerca quins restaurants satisfan la cerca i n'escriu una \
        llista numerada (12 elements com a molt). Per exemple: /find pizza. \n\
        /info <numero>: mostra la informació sobre el restaurant especificat pel \
        seu número (triat de la darrera llista numerada obtinguda amb /find).\n\
        /guide <numero>: mostra un mapa amb el camí més curt per anar del punt \
        actual on es troba l'usuari al restaurant especificat pel seu número \
        (triat de la darrera llista numerada obtinguda amb /find).")

    def start(self, update, context) -> None:
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "Hola! Soc un bot per trobar la ruta més ràpida al restaurant que vulguis de Barcelona. Fes servir /help per obtenir informació sobre les comandes que puc executar, i activa l'opció de compartir la localització amb el bot per tal de poder començar aquesta aventura")

    def update_location(self,update,context) -> None:
        self.coord[0] = update.edited_message['location']['latitude']
        self.coord[1] = update.edited_message['location']['longitude']

    def get_location(self, update, context) -> None:
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "La teva localització actual és (" + str(self.coord[0]) + "," + str(self.coord[1]) + ")")

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



def main():

    token = ""
    try:
        token = open('token.txt').read().strip()
    except FileNotFoundError:
        sys.exit("It seems the token to access the bot is not in the same directory as the bot")

    bot = Bot()
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.location, bot.update_location))
    dispatcher.add_handler(CommandHandler('get_location', bot.get_location))
    dispatcher.add_handler(CommandHandler('start', bot.start))
    dispatcher.add_handler(CommandHandler('help', bot.help))
    dispatcher.add_handler(CommandHandler('author', bot.author))
    dispatcher.add_handler(CommandHandler('find', bot.find))
    dispatcher.add_handler(CommandHandler('info', bot.info))
    dispatcher.add_handler(CommandHandler('guide', bot.guide))

    updater.start_polling()

if __name__ == "__main__":
    main()
