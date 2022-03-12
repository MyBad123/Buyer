# Buyer
Buyer is an application for searching for goods in Google and Yandex search engines. This system takes search results from search engines and analyzes the content of sites for the presence of goods, prices and contacts.

##### Advantages of this system:

- Quick search
- Quick Analysis
- Convenient output of results

# How to start?
##### What needs to be installed

- [Python3](https://www.python.org) - programming language
- [Rabbidmq](https://www.rabbitmq.com) - app for celery work

##### Install dependencies to virtual enviroment(after clone project):
####
```sh
virtualenv env
pip install -r requirements.txt
```

##### Create db and migrate struct of db from django:
####
```sh
sudo -u postgres psql
CREATE DATABASE b2b;
CREATE USER buyer_user WITH PASSWORD 'KJNjkjnkerKJNEKRF3456';
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE b2b TO buyer_user;
\q
python3 manage.py makemigrations
python3 manage.py migrate
```

##### Run app:
####
```sh
python3 manage.py runserver 0.0.0.0:8000
```

# Delete db and create it without migrations
##### Delete migrations: 
####
```sh
rm -rf app/migrations
mkdir app/migrations
touch app/migrations/__init__.py
```
##### Recreate db:
####
```sh
sudo -u postgres psql
DROP DATABASE b2b;
CREATE DATABASE b2b;
GRANT ALL PRIVILEGES ON DATABASE b2b TO buyer_user;
\q
```
##### Commands for migrations:
####
```sh
python3 maange.py makemigrations
python3 manage.py migrate
```
# Work with celery
Celery is a queuing program. This is an important part of the whole project. To run celery, you need the rabbitmq broker, which was recommended to be installed at the beginning of the documentation.

##### Command to run celery: 
####
```sh
celery -A Buyer worker -l INFO
```

# Flake8
[Flake8](https://flake8.pycqa.org/en/latest/#) is is a great toolkit for checking your code base against coding style (PEP8), programming errors (like “library imported but unused” and “Undefined name”) and to check cyclomatic complexity.

##### Test everything in the current directory:
####
```sh
flake8 
```

##### Test everything in the given directory:
####
```sh
flake8 ./directory
```

##### Test some file:
####
```sh
flake8 file.py
```
