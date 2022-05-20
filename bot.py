import os
import sys
import restaurants
import city
from nodes import *
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from typing_extensions import TypeAlias
from typing import Dict, List
import os


class Bot:
    street_graph: TypeAlias = city.OsmnxGraph
    city_graph: TypeAlias = city.CityGraph
    all_restaurants: TypeAlias = restaurants.Restaurants
    res_list: TypeAlias = Dict[int, restaurants.Restaurants]
    coord: TypeAlias = Dict[int, List[int]]  # (latitude, longitude)

    def __init__(self) -> None:
        self.street_graph = city.load_osmnx_graph("graph.gpickle")
        self.city_graph = city.load_city_graph("graph.gpickle",
                                               "city_graph.gpickle")
        self.all_restaurants = restaurants.read()
        self.res_list = {}
        self.coord = {}

    def start(self, update, context) -> None:
        """Escriu el missatge inicial del bot."""
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=open("start.txt").read())

    def help(self, update, context) -> None:
        """
        Escriu l'especificació de totes les comandes que l'usuari pot
        utilitzar amb el bot.
        """
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=open("help.txt").read())

    def update_location(self, update, context) -> None:
        """Guarda la localització de l'usuari quan aquest la comparteix."""
        id = update.message.from_user.id  # id usuari
        self.coord[id] = [0, 0]
        self.coord[id][0] = update.message['location']['longitude']
        self.coord[id][1] = update.message['location']['latitude']
        print("user", id, "has updated his location.")

    def get_location(self, update, context) -> None:
        """
        Escriu les coordenades de la ubicació des de la qual es traçaran
        les rutes.
        """
        id = update.message.from_user.id  # id usuari
        if id not in self.coord.keys():
            txt = "No tenim la teva ubicació. Envia-la. Si ja l'has enviat pot"
            txt += " tardar una estona en carregar."
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

    def author(self, update, context):
        """
        Escriu qui ha fet el programa.
        """
        txt = "Aquest programa està fet per Oriol López i Thomas González."
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=txt)

    def find(self, update, context):
        """
        Donada una paraula per filtrar, escriu tots els restaurants de Barcelona
        amb la paraula a algun camp seu (nom, descripció, ubicació etc.)
        """
        query = str(context.args[0])
        id = update.message.from_user.id  # id usuari
        restaurants.find(query, self.all_restaurants)
        self.res_list[id] = restaurants.find(query, self.all_restaurants)
        if len(self.res_list) == 0:
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

    def info(self, update, context):
        """
        Donat el número del restaurant a la llista de la última cerca,
        escriu tota la seva informació.
        """
        id = update.message.from_user.id  # id usuari
        if id not in self.res_list.keys():
            txt = "Has de buscar restaurants amb la comanda /find <query> abans"
            txt += " de buscar la informació d'algun restaurant."
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
                txt = ""
                for attribute, value in vars(self.res_list[id][numero]).items():
                    txt += str(attribute) + ": " + str(value) + "\n"
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=txt)

    def guide(self, update, context):
        """
        Donat el número del restaurant a la llista de la última cerca,
        mostra a pantalla un mapa de com arribar-hi.
        """
        id = update.message.from_user.id  # id usuari
        if id not in self.res_list.keys():
            txt = "Has de buscar restaurants amb la comanda /find <query> "
            txt += "abans de buscar la informació d'algun restaurant."
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
                city.plot_path(self.city_graph, city.find_path(self.street_graph,
                                                               self.city_graph, self.coord[id], restaurant_pos),
                               "path" + str(id) + ".png")
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open("path" + str(id) + ".png", 'rb'))
                os.remove("path" + str(id) + ".png")


def main():
    """
    Crea un bot de telegram que permet trobar i arribar a restaurants
    de Barcelona.
    """
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
    updater.start_polling()


if __name__ == "__main__":
    main()
