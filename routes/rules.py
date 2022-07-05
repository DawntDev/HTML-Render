from flask import render_template
from tools import Manager

def rules(version):
    app = Manager.getItem('app')
    
    root = {}
    for rule in app.url_map.iter_rules():
        if not rule.rule in ("/rules", "/static/<path:filename>", "/<regex('(.*?)\.(html|png|jpg)$'):file>"):
            root[rule.rule] = *filter(lambda x: x in ("GET", "POST", "PUT", "DELETE"), rule.methods),
    
    root = {rule: methods for rule, methods in root.items() if version in rule}
    print(root)
    
    return render_template("rules.html", rules=root)