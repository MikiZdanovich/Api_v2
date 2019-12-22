# Api_v2
Restfull APi with flask 2.0

## How to run project

# Build images with app and postrgresql bd
docker-compose build

# Up services
docker-compose up -d

# Run migrations
docker-compose run --rm app python manage.py db upgrade

Open http://localhost:5000/
