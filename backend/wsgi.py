import os
from apps import create_app
from app.main.views import user_bp

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run()
