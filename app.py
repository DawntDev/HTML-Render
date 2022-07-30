from flask import Flask, render_template
from flask_cors import CORS
from routes import ROOT
from src.tools import RegexConverter, Manager, PATH
from src.html_render import HTMLRender
from threading import Timer
import os
import shutil

# Create a new Flask application
app = Flask(__name__, template_folder="public", static_folder="public/static")
app.url_map.converters['regex'] = RegexConverter
app.config['SECRET_KEY'] = 'secret'
CORS(app)
Manager.app = app


# Regenerate the builds folder
if os.path.exists("public/builds"):
    shutil.rmtree("public/builds")
os.mkdir("public/builds")
Manager.builds = []

# Not found route
@app.errorhandler(404)
def not_found(error):
    return render_template("not-found.html"), 404

# Register the routes
for route in ROOT:
    app.route(
        rule=route["path"],
        methods=route["methods"]   
    )(route['func'])

if __name__ == "__main__":
    Timer(.25, HTMLRender.init, args=(PATH,)).start()
    print("\n\x1b[1;32m[Flask]\x1b[0m - Initializing...\n")
    app.run()