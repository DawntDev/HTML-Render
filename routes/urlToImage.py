from flask import request, url_for

def urlToImage():
    if request.method == "POST":
        pass
    url  = request.args.get("url")
    return "URL to image"