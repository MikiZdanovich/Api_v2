import os

from app import blueprint
from app.main import create_app
from werkzeug.middleware.proxy_fix import ProxyFix


app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.wsgi_app = ProxyFix(app.wsgi_app)
app.register_blueprint(blueprint)

app.app_context().push()