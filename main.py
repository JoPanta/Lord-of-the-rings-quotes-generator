import requests
from random import randint

URL = "https://the-one-api.dev/v2/"
API_KEY = "c1JSdFXNxqBnlRC1Xh3R"
headers = {'Authorization': 'Bearer c1JSdFXNxqBnlRC1Xh3R'}

quote_data = requests.get(url=f"{URL}/quote", headers=headers)
quote_data.raise_for_status()
data = quote_data.json()


random_number = randint(0,999)
quote_json = data["docs"][random_number]

# getting quote
quote = quote_json["dialog"]

# getting character's name
character_id = quote_json["character"]
character_data = requests.get(url=f"{URL}character/{character_id}", headers=headers)
character_data.raise_for_status()
character_json = character_data.json()
character = character_json['docs'][0]["name"]

# getting quote movie
movie_id = quote_json["movie"]
movie_data = requests.get(url=f"{URL}movie/{movie_id}", headers=headers)
movie_data.raise_for_status()
movie_json = movie_data.json()
movie = movie_json['docs'][0]['name']

# getting character wiki link
try:
    wiki_link = character_json['docs'][0]["wikiUrl"]
except (ValueError, RuntimeError, TypeError, NameError):
    wiki_link = None

print(quote)
print(character)
print(movie)
print(wiki_link)

