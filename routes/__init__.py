from routes.index import index
from routes.render import render
from routes.urlToImage import urlToImage
from routes.builds import builds
from routes.rules import rules

ROOT = [
    {
        "path": "/",
        "func": index,
        "methods": ["GET"]
    },
    {
        "path": "/api/v1/render",
        "func": render,
        "methods": ["POST"],
    },
    {
        "path": "/api/v1/urlToImage",
        "func": urlToImage,
        "methods": ["GET", "POST"],
    },
    {
        "path": "/api/v1/builds/<regex('(.*?)\.(html|png|jpg|txt)$'):file>",
        "func": builds,
        "methods": ["GET"],
    },
    {
        "path": "/rules/<string:version>",
        "func": rules,
        "methods": ["GET"],
    }
]