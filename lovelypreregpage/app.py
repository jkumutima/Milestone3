import flask
import json
from flask import Flask, g, render_template, jsonify, request
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin
import shelve

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://dlmjtbasqxmjsb:1f06bd9e0fb588659a025e5c54c609d9ff0804f85edd7e7e851fdc12b79fbaa5@ec2-34-203-91-150.compute-1.amazonaws.com:5432/db4rp6bvjk6v34'

cors = CORS(app)
api = Api(app)
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<E-mail %r>' % self.email
    def serialize(self):
        return {'email': self.email}    

class Song(db.Model):
    __tablename__ = "songs" 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False)
    artist = db.Column(db.String(120), unique=False)
    
    def __init__(self, name, artist):
        self.name = name
        self.artist = artist
        
    def __repr__(self):
        return '<%s by %s>' % self.name, self.artist  
    def serialize(self):
        return {'name': self.name, 'artist': self.artist}         

# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')

# Save e-mail to database and send to success page
@app.route('/prereg', methods=['POST'])
def prereg():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email, password)
            db.session.add(reg)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if  db.session.query(User).filter(User.email == email, User.password == password).count(): 
            return flask.redirect("/songs") 
        else:
            return flask.redirect("/")  
    return render_template('index.html')

@app.route('/logino', methods=['POST'])
def logino():
    email = None

    if request.method == 'POST' : #and "email" in request.form and "password" in request.form:
        form = request.get_json()
        email = form['email']
        password = form['password']
        if  db.session.query(User).filter(User.email == email, User.password == password).count(): 
            return {'message': 'you are logged in'}, 200 
        else:
            return {'message': 'invalid email or password'}, 401  
    return {'message': 'please login'}, 400

#sign up
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email, password)
            db.session.add(reg)
            db.session.commit()
            return flask.redirect("/")
    return render_template('signup.html')  

@app.route('/signupu', methods=['POST'])
def signupu():
    email = None
    if request.method == 'POST':
        email = request.get_json()['email']
        password = request.get_json()['password']
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email, password)
            db.session.add(reg)
            db.session.commit()
            return {'message': 'registration successful'}, 200 
        else:
            return {'message': 'user already exist'}, 409  
    return {'message': 'sign up credintials denied'}, 400

#songs
@app.route('/songs', methods=['GET', 'POST'])
def songs():
    songs = []
    error = None
    song = None
    artist = None
    if request.method == 'POST':
        song = request.form['song']
        artist = request.form['artist']
        
    
        if song is not None:
            print("song", song)
            if artist is None or artist.strip()=="":
                songs = db.session.query(Song).filter(Song.name == song).all()
            else:
                songs = db.session.query(Song).filter(Song.name == song, Song.artist == artist).all()    
        elif artist is not None and artist.strip()!= "":
            songs = db.session.query(Song).filter(Song.artist == artist).all()   
        else:
            error = "no song found"
           
        if len(songs)== 0:
            error = "no song found"
    return render_template('songs.html', songs= songs, error =error)   

@app.route('/chanson', methods=['GET'])
def query_songs():
    songs = db.session.query(Song).all()
    #song1 = {'name': songs[0].name, 'id': songs[0].id, 'artist': songs[0].artist}
    return json.dumps(list(map(lambda x: x.serialize(), songs)))


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

@app.route('/newsonga', methods=['PUT'])
def newsonga():
    if request.method == 'PUT' and "song" in request.form and "artist" in request.form: 
        song = request.get_json()['song']
        artist = request.get_json()['artist']
        if song is None or song == "" or artist is None or artist == "":
            return {'message': 'invalid data'},400
        if not db.session.query(Song).filter(Song.name == song).count():
            reg = Song(song, artist)
            db.session.add(reg)
            db.session.commit()
            return {'message': "song created"}, 200
        else:
            return {'message': 'song already exist'}, 409 
    return {'message': 'song was not received'}, 400 

  
@app.route('/users', methods=['GET'])
def query_users():
    users = db.session.query(User).all()
    #user1 = {"email": "Jkumutima@.com"}
    #user1 = {'email': users[0].email, 'id': users[0].id, 'password': users[0].password}
    return json.dumps(list(map(lambda x: x.serialize(), users)))



if __name__ == '__main__':
    app.debug = True
    app.run()
