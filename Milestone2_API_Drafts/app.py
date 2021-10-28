import flask
import json
from flask import Flask, render_template, jsonify, request
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://dlmjtbasqxmjsb:1f06bd9e0fb588659a025e5c54c609d9ff0804f85edd7e7e851fdc12b79fbaa5@ec2-34-203-91-150.compute-1.amazonaws.com:5432/db4rp6bvjk6v34'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
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
        # Check that email does not already exist (not a great query, but works)
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


''' 
data = request.get_json()     # status code
        return jsonify({'data': data}

        data: {
                email: email,
                password: pwd
            }
''' 


#sign up
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email, password)
            db.session.add(reg)
            db.session.commit()
            return flask.redirect("/")
    return render_template('signup.html')  

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

#api  

@app.route('/users', methods=['GET'])
def query_users():
    users = db.session.query(User).all()
    #user1 = {"email": "Jkumutima@.com"}
    user1 = {'email': users[0].email, 'id': users[0].id, 'password': users[0].password}
    return json.dumps(user1)

''' 
@app.route('/login', methods=['POST'])
#get email and ppwd from request body ( sent from front end )
#Query in user info in db using provided email
#if there is no email in db return response = {status: 500, message: 'fail'}
# Compare usr pwd from db and user pwd from front end to see if they are the same
# if passwrd do not match status: response ={ 500, message: 'fail'}
# if password match and email exist response = { status: 200, message: 'success'}

    return json.dumps(response)


@app.route('/signup', methods=['POST'])
#get email and ppwd from request body ( sent from front end )
# Add user to db 
# If add user to db is success response { status: 200, message: 'success'}
# else response = {status: 500, message: 'fail'}

    return json.dumps(response)

@app.route('/song/songName', methods=['GET'])
#get song name from pathParmeter
# Fetch song Info from dd
# if there is no song of this title return response = {status: 500, message: 'fail'}
# else if there a song of this title return {status: 200, data: {name: '', artist:''}}

    return json.dumps(response)

@app.route('/song/artistName', methods=['GET'])
#get artist name from pathParmeter
# Fetch song Info from dd
# if there is no song of this artist return response = {status: 500, message: 'fail'}
# else if there a song of this artist return {status: 200, data: {name: '', artist:''}}

    return json.dumps(response)

@app.route('/song', methods=['POST'])

#get song Info from request body ( sent from front end )
# Add song to db 
# If add song to db is success response { status: 200, message: 'success'}
# else response = {status: 500, message: 'fail'}

    return json.dumps(response)

'''
@app.route('/chanson', methods=['GET'])
def query_songs():
    songs = db.session.query(Song).all()
    song1 = {'name': songs[0].name, 'id': songs[0].id, 'artist': songs[0].artist}

    return json.dumps(song1)


# convert into JSON:
#y = json.dumps(x)

# the result is a JSON string:
#print(y) # do return

#json = requests.get(url).json()




if __name__ == '__main__':
    app.debug = True
    app.run()
