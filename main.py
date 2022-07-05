from flask import Flask
from flask_cors import CORS
from routes import ROOT
from tools import RegexConverter, Manager


app = Flask(__name__, template_folder="public")
app.url_map.converters['regex'] = RegexConverter
app.config['SECRET_KEY'] = 'secret'
CORS(app)
Manager(app=app)

for i in ROOT: app.route(i['path'], methods=i['methods'])(i['func'])

if __name__ == "__main__":
    app.run(debug=True)