# Api_v2
Restfull APi with flask 2.0

## How to run project

# Build images with app and postrgresql bd
docker-compose build

# Up services
docker-compose up -d

# Run migrations for first time up app
docker-compose exec app python manage.py db init
docker-compose exec app python manage.py db migrate
# Run migrations 
docker-compose exec app python manage.py db upgrade


Open http://localhost:5000/
