# path = [
#     {
#         "path": "/api/v1/render",
#         "func": render,
#         "methods": ["POST"],
#     },
#     {
#         "path": "/api/v1/urlToImage",
#         "func": url_to_image,
#         "methods": ["GET", "POST"],
#     },
#     {
#         "path": r"/api/v1/builds/<regex('(.*?)\.(html|png|jpg|bin|base64)$'):file>",
#         "func": builds,
#         "methods": ["GET"],
#     }
# ]

from .common import common
from .api import api