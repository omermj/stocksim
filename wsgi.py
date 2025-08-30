from werkzeug.middleware.proxy_fix import ProxyFix
from app import app as flask_app

# Keep ProxyFix to respect X-Forwarded-* headers behind proxies
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_prefix=1, x_proto=1, x_host=1)

# Export the Flask app directly at the root path
app = flask_app
