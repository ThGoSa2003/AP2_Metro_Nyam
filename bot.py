import restaurants
import city
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from typing import Dict
import os
from typing_extensions import TypeAlias
from typing import Union, List, Tuple
from metro import Position


class Bot:
    """This class represents the Bot."""
    st_graph: TypeAlias = city.OsmnxGraph
    city_graph: TypeAlias = city.CityGraph
    all_restaurants: TypeAlias = restaurants.Restaurants
    res_list: TypeAlias = Dict[int, restaurants.Restaurants]
    # user_id: Restaurants
    coord: TypeAlias = Dict[int, Position]
    # user_id: (longitude, latitude)

    def __init__(self) -> None:
        """Initilization of the bot instance."""
        self.st_graph = city.load_osmnx_graph("graph.gpickle")
        self.city_graph = city.load_city_graph("graph.gpickle",
                                               "city_graph.gpickle")
        self.all_restaurants = restaurants.read()
        self.res_list = {}
        self.coord = {}

    def start(self, update, context) -> None:
        """It writes the first message of the conversation."""
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=open("start.txt").read())
        print("Usuari", update.message.from_user.id, "ha fet /start")

    def help(self, update, context) -> None:
        """
        It writes the specification of all the commands that are
        available for the user.
        """
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=open("help.txt").read())
        print("Usuari", update.message.from_user.id, "ha fet /help")

    def update_location(self, update, context) -> None:
        """It saves the user's location when he/she sends it."""
        id = update.message.from_user.id  # user id
        long = update.message['location']['longitude']
        lat = update.message['location']['latitude']
        self.coord[id] = (long, lat)
        print("Usuari", id, "ha actualitzat la seva ubicació")

    def get_location(self, update, context) -> None:
        """
        It writes the coordinates from which the routes will be calculated.
        """
        id = update.message.from_user.id  # user id
        if id not in self.coord.keys():
            txt = "No tenim la teva ubicació. Envia-la. Si ja l'has enviat"
            txt += " pot tardar una estona en carregar."
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=txt)
        else:
            id = update.message.from_user.id
            txt = "La teva localització actual és (" + str(self.coord[id][0])
            txt += "," + str(self.coord[id][1]) + ")"
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=txt)
        print("Usuari", id, "ha fet /get_location")

    def author(self, update, context):
        """ It writes the authors of the program."""
        txt = "Aquest programa està fet per Oriol López i Thomas González."
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=txt)
        print("Usuari", update.message.from_user.id, "ha fet /author")

    def find(self, update, context):
        """
        Given a logical query entry in the user context, write some
        restaurants (up to 12) which gat through the filter.
        """
        if len(context.args) == 0:
            return
        query = ''
        for a in context.args:
            query += a
        id = update.message.from_user.id  # user id
        self.res_list[id] = restaurants.find(query,
                                             self.all_restaurants)

        if len(self.res_list[id]) == 0:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="No hem trobat cap restaurant amb aquest filtre.")
        else:
            txt = ""
            length = len(self.res_list[id])
            if length > 12:
                length = 12
            for i in range(length):
                txt += str(i) + " " + str(self.res_list[id][i].name) + "\n"
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=txt)
        print("Usuari", id, "ha fet /find")

    def info(self, update, context):
        """
        Given the number of the restaurant in the last list obtained with the
        find command, write all its information.
        """
        id = update.message.from_user.id  # user id
        if id not in self.res_list.keys():
            txt = "Has de buscar restaurants amb la comanda /find <query>"
            txt += " abans de buscar la informació d'algun restaurant."
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=txt)
        else:
            num = int(context.args[0])
            if num < 0 or num >= len(self.res_list[id]):
                txt = "El número de restaurant que has introduït no és a la "
                txt += "llista de cerca més recent."
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=txt)
            else:
                res = self.res_list[id][num]
                txt = "Nom: " + str(res.name) + "\n"
                txt += "Adreça: " + str(res.adresses_road_name)
                if res.adresses_start_street_number is not None:
                    txt += " " + str(int(res.adresses_start_street_number))
                txt += "\n" + "Districte: "
                txt += str(res.adresses_neighbourhood_name) + ", "
                txt += str(res.adresses_district_name) + "\n"
                txt += str(res.values_attribute_name) + str(res.values_value)

                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=txt)
        print("Usuari", id, "ha fet /info")

    def guide(self, update, context):
        """
        Given the number of the restaurant in the last list obtained with the
        find command, show in the map how to arrive to it from the user's
        location..
        """
        id = update.message.from_user.id  # user id
        if id not in self.res_list.keys():
            txt = "Has de buscar restaurants amb la comanda /find <query> "
            txt += "abans de buscar la informació d'algun restaurant."
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=txt)
        elif id not in self.coord.keys():
            txt = "Has de compartir la teva ubicació "
            txt += "si vols que pugui guiar-te."
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=txt)
        else:
            numero = int(context.args[0])
            if numero < 0 or numero >= len(self.res_list[id]):
                txt = "El número de restaurant que has introduït no és a la "
                txt += "llista de cerca més recent."
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=txt)
            else:
                restaurant = self.res_list[id][numero]
                res_long = restaurant.geo_epgs_4326_y
                res_lat = restaurant.geo_epgs_4326_x
                restaurant_pos = (res_long, res_lat)
                city.plot_path(self.city_graph,
                               city.find_path(self.st_graph,
                                              self.city_graph, self.coord[id],
                                              restaurant_pos),
                               "path" + str(id) + ".png")
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open("path" + str(id) + ".png", 'rb'))
                os.remove("path" + str(id) + ".png")
        print("Usuari", id, "ha fet /guide")


def main():
    """Deploy the bot in telegram."""
    token = ""
    try:
        token = open('token.txt').read().strip()
    except FileNotFoundError:
        txt = "It seems the token to access the bot is not in the same "
        txt += "directory as the bot"
        sys.exit(txt)

    bot = Bot()
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.location,
                                          bot.update_location))
    dispatcher.add_handler(CommandHandler('get_location', bot.get_location))
    dispatcher.add_handler(CommandHandler('start', bot.start))
    dispatcher.add_handler(CommandHandler('help', bot.help))
    dispatcher.add_handler(CommandHandler('author', bot.author))
    dispatcher.add_handler(CommandHandler('find', bot.find))
    dispatcher.add_handler(CommandHandler('info', bot.info))
    dispatcher.add_handler(CommandHandler('guide', bot.guide))
    print("Bot iniciat")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
