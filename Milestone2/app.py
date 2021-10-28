import flask
from flask import Flask, render_template, request
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://dlmjtbasqxmjsb:1f06bd9e0fb588659a025e5c54c609d9ff0804f85edd7e7e851fdc12b79fbaa5@ec2-34-203-91-150.compute-1.amazonaws.com:5432/db4rp6bvjk6v34'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
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

if __name__ == '__main__':
    app.debug = True
    app.run()
