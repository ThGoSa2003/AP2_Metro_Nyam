import pandas as pd
import fuzzysearch
from dataclasses import *
from typing import Optional, List

@dataclass
class Restaurant:
    """
    Implementation of the Restaurant class.
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
    geo_epgs_25831_y: int
    geo_epgs_4326_x: float
    geo_epgs_4326_y: float

    def contains(self, query: str) -> bool:
        """
        Returns whether the restaurant contains a given word "query" in any
        of its attributes.
        """

        for attribute, value in vars(self):
            if value == query:
                return True
        return False

Restaurants = List[Restaurant]


def read() -> Restaurants:
    csv_restaurants = pd.read_csv('https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/restaurants.csv')
    dim = csv_restaurants.shape
    l = Restaurant(*[i for i in csv_restaurants.iloc[0,:]])
    print(l)
    fields = dir(Restaurant)
    for i in range(len(l)):
        R.fields[i] = l[i]

    r = Restaurant(i for i in csv_restaurants.iloc[0,:][:])
    print(r)
    #for i in range(dim[0]):
    #    print(csv_restaurants.iloc[i,:])

read()


def find(query: str, restaurants: Restaurants) -> Restaurants:
    """
    Given a word "query", return the list of restaurants with that word in
    any of its attributes.
    """

    filtered_list = [restaurant for restaurant in restaurants if restaurant.contains(query)]
