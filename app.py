from flask import Flask
from flask_cors import CORS
from routes import ROOT
from src.tools import RegexConverter, Manager, PATH
from src.html_render import HTMLRender
from threading import Thread
import os
import shutil

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

# Register the routes
for route in ROOT:
    app.route(
        rule=route["path"],
        methods=route["methods"]   
    )(route['func'])

if __name__ == "__main__":
    Thread(target=HTMLRender.init, args=(PATH,)).start()
    app.run()
