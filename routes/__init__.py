from routes.index import index
from routes.new_render import new_render
from routes.render import render
from routes.url_to_image import url_to_image
from routes.builds import builds
from routes.rules import rules

ROOT = [
    {
        "path": "/",
        "func": index,
        "methods": ["GET"]
    },
    {
        "path": "/new-render",
        "func": new_render,
        "methods": ["GET"]
    },
    {
        "path": "/api/v1/render",
        "func": render,
        "methods": ["POST"],
    },
    {
        "path": "/api/v1/urlToImage",
        "func": url_to_image,
        "methods": ["GET", "POST"],
    },
    {
        "path": "/api/v1/builds/<regex('(.*?)\.(html|png|jpg|bin|base64)$'):file>",
        "func": builds,
        "methods": ["GET"],
    },
    {
        "path": "/api/rules/<string:version>",
        "func": rules,
        "methods": ["GET"],
    }
]
