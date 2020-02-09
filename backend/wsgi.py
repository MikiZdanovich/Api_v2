import os
from apps import create_app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

if __name__ == "__main__":
    app.run()
