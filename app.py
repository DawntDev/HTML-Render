from flask import Flask, redirect
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
for i in ROOT:
    app.route(i['path'], methods=i['methods'])(i['func'])


@app.route('/test')
def test():
    exist = HTMLRender.screenshot("https://www.google.com")
    print(exist)
    return redirect("api/v1/builds/test.png")

if __name__ == "__main__":
    Thread(target=HTMLRender.init, args=(PATH,)).start()
    app.run()
