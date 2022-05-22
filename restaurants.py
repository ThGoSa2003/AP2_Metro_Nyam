import fuzzysearch
import sys
import pandas as pd
from dataclasses import *
from typing import Optional, List
from typing_extensions import TypeAlias
from fuzzysearch import find_near_matches


@dataclass
class Restaurant:
    """
    This class represents a restaurant of the city of Barcelona

    All the atributes from the csv will be added to this class
    """

    register_id: int
    name: str
    institution_id: Optional[int]
    institution_name: Optional[int]
    created: str
    modified: str
    adresses_roadtype_id: Optional[int]
    adresses_roadtype_name: Optional[str]
    adresses_road_id: int
    adresses_road_name: str
    adresses_start_street_number: int
    adresses_end_street_number: Optional[int]
    adresses_neighbourhood_id: int
    adresses_neighbourhood_name: str
    adresses_district_id: int
    adresses_district_name: str
    adresses_zip_code: int
    adresses_town: str
    adresses_main_adress: bool
    adresses_type: Optional[str]
    values_id: int
    values_attribute_id: int
    values_category: str
    values_attribute_name: str
    values_value: int
    values_outstanding: int
    values_description: str
    secondary_filters_id: int
    secondary_filters_name: str
    secondary_filters_fullpath: str
    secondary_filters_tree: int
    secondary_filters_asia_id: int
    geo_epgs_25831_x: float
    geo_epgs_25831_y: float
    geo_epgs_4326_x: float
    geo_epgs_4326_y: float

    def contains(self, query: str) -> bool:
        """
        :param query: a word that you want to serch in the restaurants
        :returns: whether if query is in any of the attributes
        """

        for attribute, value in vars(self).items():
            if query.lower() in str(value).lower():
                return True
        return False

    def contains(self, query: str) -> bool:
        """
        :param query: a word that you want to serch in the restaurants
        :returns: whether if query is in any of the attributes
        """
        query = query.lower()
        for attribute, value in vars(self).items():
            v = str(value).lower()
            if find_near_matches(query, v, max_l_dist = 1) != []:
                return True
        return False


Restaurants: TypeAlias = List[Restaurant]


def read() -> Restaurants:
    """
    :returns: a list of the restaurants of Barcelona
    """

    try:
        csv_res = pd.read_csv('./data/restaurants.csv')
        dim = csv_res.shape
        restaurants = []
        for i in range(dim[0]):
            restaurants.append(Restaurant(*[j for j in csv_res.iloc[i, :]]))
        return restaurants
    except Exception:
        sys.exit("I cannot find the data/restaurants.csv, please add it in it")


def find(query: str, restaurants: Restaurants) -> Restaurants:
    """
    :param restaurants: a list of restaurants
    :param query: a word you want to serch for in the restaurants
    :returns: a list of the restaurants that contain query in any field
    """

    return [r for r in restaurants if r.contains(query)]
