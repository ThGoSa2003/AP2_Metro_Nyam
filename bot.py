import restaurants
from city import St_node
import city
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from typing import List

class Bot:
    st_graph: city.OsmnxGraph
    city_graph: city.CityGraph
    restaurants: restaurants.Restaurants
    restaurants_of_the_search: restaurants.Restaurants
    coord = List[int] # (latitude, longitude)


    def __init__(self) -> None:
        self.st_graph = city.load_osmnx_graph("graph")
        self.city_graph = city.load_city_graph("graph", "city_graph")
        self.restaurants = restaurants.read()
        self.restaurants_of_the_search = []
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
        self.restaurants_of_the_search = restaurants.find(query, self.restaurants)
        txt = ""
        for i in range(len(self.restaurants_of_the_search)):
            txt += str(i) + " " + str(self.restaurants_of_the_search[i].name) + "\n"
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=txt)

    def info(self, update, context):
        numero = int(context.args[0])
        print("Informació de", self.restaurants_of_the_search[numero])
        txt = ""
        for attribute, value in vars(self.restaurants_of_the_search[numero]).items():
            txt += str(attribute) + ": " + str(value) + "\n"
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=txt)

    def guide(self, update, context):
        numero = int(context.args[0])
        restaurant = self.restaurants_of_the_search[numero]
        restaurant_pos = (restaurant.geo_epgs_25831_x, restaurant.geo_epgs_25831_y)
        city.plot_path(self.city_graph, city.find_path(self.st_graph,
            self.city_graph, self.coord,
            restaurant_pos),
            "path")
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open("path.png", 'rb'))
        os.remove("path.png")



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
