from types import TracebackType
import flask
from flask import Flask, render_template, request, redirect, session, jsonify, url_for
#import flask
#from flask import render_template
#from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random
#import requests
import os
import spotipy
from dotenv import find_dotenv,load_dotenv
load_dotenv(find_dotenv())
from spotipy.oauth2 import SpotifyClientCredentials
from env import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, GENIUS_TOKEN



artist_id = '1uNFoZAHBGtllmzznpCI3s'
artist_uri = 'spotify:artist:{}'.format(artist_id)

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://dlmjtbasqxmjsb:1f06bd9e0fb588659a025e5c54c609d9ff0804f85edd7e7e851fdc12b79fbaa5@ec2-34-203-91-150.compute-1.amazonaws.com:5432/db4rp6bvjk6v34'
# suppresses a warning - not strictly needed
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# define some Models!
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    song = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}"

db.create_all()


#db.session.add(User="Flask", song="love yourself"))
db.session.commit()
#users = User.query.all()
#class Artist(id,):
@app.route("/")
def main():
    return flask.render_template("Login.html")



#new song
@app.route('/newsong', methods=['POST', 'GET'])
def newsong():
    if request.method == 'POST':
        song = request.form['song']
        artist = request.form['artist']
        if not db.session.query(Song).filter(Song.name == song).count():
            reg = Song(song, artist)
            db.session.add(reg)
            db.session.commit()
            return flask.redirect("/songs")
    return render_template('songs.html') 








@app.route("/login", methods=["POST"])
def login():
    #if request.method == "POST":    
    val = flask.request.form["username"]
    val2 = User.query.filter_by(username=val).first() 

    if val == val2.username:     
         return flask.redirect("welcome")
    else:
        flask.flash("Wrong username!")  
    return flask.redirect("/")
    return flask.render_template('login.html')      

@app.route("/")
def sign():
    return flask.render_template("signup.html")

@app.route("/", methods=["GET", "POST"])
def index():
    spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))
    top_five = spotify_client.artist_top_tracks(artist_uri)
    
    random_song = random.choice(top_five['tracks'])
    
    users = User.query.all()
    usernames = []
    songs = []
    for user in users:
        usernames.append(user.username)
        songs.append(user.song)
    
    if flask.request.method == "POST":
        username = flask.request.form.get('username')
        song = flask.request.form.get('song')
        user = User(username=username)
        songname =User(song=song)
        db.session.add(user)
        db.session.add(songname)
        db.session.commit()
        username.append(username)
        song.append(song)
        return flask.jsonify({"response": "Saved a new Users"})
    
    return flask.render_template( "index2.html", length=len(username), username=username, song=song, users = User.query.all()
)


#app.run(debug=True)

if __name__ == '__App__':
   app.debug = True
   app.run()
