from flask import render_template
from src.tools import Manager

def rules(version):
    app = Manager.app

    root = []
    for rule in app.url_map.iter_rules():
        if not rule.rule in ("/rules", "/static/<path:filename>", "/api/v1/builds/<regex('(.*?)\.(html|png|jpg|bin|base64)$'):file>"):
            if version in rule.rule:
                root.append([rule.rule, [*filter(lambda x: x in ("GET", "POST", "PUT", "DELETE"), rule.methods)]])
    return render_template("rules.html", rules=root)
