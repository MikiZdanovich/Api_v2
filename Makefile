.PHONY: clean system-packages python-packages install tests run all

clean:
   find . -type f -name '*.pyc' -delete
   find . -type f -name '*.log' -delete

system-packages:
   sudo apt install python-pip -y

python-packages:
   pip install -r requirements.txt

install: system-packages python-packages

tests:
   python manage.py test

db_init:
   python manage.py db init
db_migrage:
	python manage.py db migrate

db_upgrade:
	python manage.py db ubgrade


run:
   python manage.py run

all: clean install tests run