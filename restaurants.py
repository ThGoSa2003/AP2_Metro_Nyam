import pandas as pd
import fuzzysearch


url = 'https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/restaurants.csv'
csv_restaurants = pd.read_csv(url)
url = 'https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/estacions.csv'
csv_restaurants = pd.read_csv(url)
url = 'https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/accessos.csv'
csv_restaurants = pd.read_csv(url)


@dataclass
class Restaurant: ...

Restaurants = List[Restaurant]


def read() -> Restaurants: ...


def find(query: str, restaurants: Restaurants) -> Restaurants: ...
