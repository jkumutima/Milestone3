import flask
import requests
import os
import spotipy
import random
from flask import render_template
from env import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, GENIUS_TOKEN
from spotipy.oauth2 import SpotifyClientCredentials


templates_folder = os.path.abspath('./templates')
static_folder = os.path.abspath('./templates')

app=flask.Flask(__name__, template_folder = templates_folder, static_folder= static_folder, static_url_path='')


artist_id = '1uNFoZAHBGtllmzznpCI3s'
artist_uri = 'spotify:artist:{}'.format(artist_id)

@app.route('/')
def index():
    spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))
    top_five = spotify_client.artist_top_tracks(artist_uri)
    
    random_song = random.choice(top_five['tracks'])

    genius_search_url = "http://api.genius.com/search?q='Justin Bieber'&access_token={}".format(GENIUS_TOKEN)
    genius_artist_response = requests.get(genius_search_url)
    genius_artist_json_data = genius_artist_response.json()
    genius_artist_hits = genius_artist_json_data['response']['hits']

    for hit in genius_artist_hits:
        cleaned_song_title = random_song['name'].replace(' (with Justin Bieber)', '')
        if cleaned_song_title in hit['result']['title']:
            random_song["lyrics_url"] = hit['result']['url']
    
    image = random_song['album']['images'][2]

    return render_template('index.html', random_song=random_song, image=image)

if __name__ == '__main__':
    app.run()