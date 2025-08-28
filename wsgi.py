from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app import app as flask_app

flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_prefix=1, x_proto=1, x_host=1)
root = Flask(__name__)
app = DispatcherMiddleware(root, {"/stocksim": flask_app})
