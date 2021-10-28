from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = APi(app)

class HelloWorld(resource):
    def get(self):
        return{"Hello World"}
        

if __name__ == '__main__':
    app.debug = True
    app.run()
