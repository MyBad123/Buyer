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

# Instructions for use
1. Go under the user 0@gmail.com (if available in the database) and password Pass@word1. If there is no password, then go to buyer.1d61.com/db / and enter the password and login of the administrator. Together with the creation of the administrator, users are created, including 0@gmail.com
2. Next, we are on the page where all applications meet us, there we can create a new application in the link "You can create a new application here", clicking on the link you need to enter 2 fields - the first field is a certain main word that will be displayed in all applications and keywords (for which it will be carried out search).
3. Next, we wait 15-20 minutes on the main page, when the search is over, the page will update the delivery status itself
4. Go to the application page. Here we can look at all the results (the top link of the "search results" section) and those selected by the scanner (with a potential product). Also, there is an opportunity to go to the correspondence that appears after sending letters (see the next paragraph).
5. Go to the scanned results, tick the box to which addresses we want to send, write the text, that's it, the letter is sent to the mail.
6. We go into correspondence - here we have all the messages that we or we have sent. here you can view all the information about the messages, we can send a message (in the corresponding section).
7. If we want to receive an incoming message, we must log in to the mail (link m.1d61.com ) under the name buyer-vendor@1d61.com and password GD38asDF348ASdf. Next, you need to send a response to the letter or enter the application number in the header or body of the letter (the application number has the form [1-1], where the numbers tend to change). After that, the letter will be processed by the parser (mail, phone numbers, full name, etc. will be displayed) and added to the table with messages.
