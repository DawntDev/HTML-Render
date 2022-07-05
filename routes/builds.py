from flask import send_from_directory

def builds(file):
    print(f"Building {file}")
    return send_from_directory("public/builds", file)
