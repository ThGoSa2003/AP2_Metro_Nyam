import pandas as pd
import fuzzysearch


url = 'https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/restaurants.csv'
csv_restaurants = pd.read_csv(url)

@dataclass
class Restaurant:
    """
    Implementation of the Restaurant class.
    """
    id: int
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


Restaurants = List[Restaurant]


def read() -> Restaurants:
    dim = csv_restaurants.shape()
    for i in range(dim[0]):


def find(query: str, restaurants: Restaurants) -> Restaurants: ...
