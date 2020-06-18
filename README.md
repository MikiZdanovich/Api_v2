# Api_v2
Restfull APi with flask 2.0

# How to run project


## Up and build required services
docker-compose -f docker-compose.yml up -d --build

## Run migrations 
docker-compose exec app alembic upgrade head

## Run service
Open http://localhost:5000/

## Run test's
Docker-compose exec app pytest