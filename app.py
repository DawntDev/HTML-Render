from flask import Flask
from flask_cors import CORS
from routes import ROOT
from src.tools import RegexConverter, Manager
import os, shutil

# Create a new Flask application
app = Flask(__name__, template_folder="public")
app.url_map.converters['regex'] = RegexConverter
app.config['SECRET_KEY'] = 'secret'
CORS(app)
Manager.app = app


# Regenerate the builds folder
if os.path.exists("public/builds"):
    shutil.rmtree("public/builds")
os.mkdir("public/builds")
Manager.builds = []

for i in ROOT: app.route(i['path'], methods=i['methods'])(i['func'])

if __name__ == "__main__":
    app.run()