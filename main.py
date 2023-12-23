import requests
from random import randint
from flask import Flask, abort, render_template, redirect, url_for, flash, request
import flask_bootstrap


URL = "https://the-one-api.dev/v2/"
API_KEY = "c1JSdFXNxqBnlRC1Xh3R"
headers = {'Authorization': 'Bearer c1JSdFXNxqBnlRC1Xh3R'}


app = Flask(__name__, static_url_path='/static')

quote_data = requests.get(url=f"{URL}/quote", headers=headers)
quote_data.raise_for_status()
data = quote_data.json()

def generate_quote():
    random_number = randint(0, 999)
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
    return quote, character, wiki_link, movie


initial_quote, initial_character, initial_wiki_link, initial_movie = generate_quote()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and request.form.get('generate_quote') == 'true':
        quote, character, wiki_link, movie = generate_quote()
        return render_template('index.html', quote=quote, character=character, movie=movie, link=wiki_link)

    return render_template('index.html', quote=initial_quote, character=initial_character, movie=initial_movie, link=initial_wiki_link)

print(initial_character)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)