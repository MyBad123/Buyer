#!/bin/bash

#перейти в каталог с проектом
cd /
cd /home/itsuppus/svetorezerv/buyer/
git stash
git stash drop
git pull
#Удалить лишние миграции
sudo rm -f /home/itsuppus/svetorezerv/buyer/app/migrations/0001_initial.py

#создаём базу
sudo -u postgres psql -f init.sql
#восстанавливаем зависимости
/home/itsuppus/svetorezerv/buyer/venv/bin/python /home/itsuppus/svetorezerv/buyer/venv/bin/pip3 install -r ./requirements.txt
#обновить миграции
/home/itsuppus/svetorezerv/buyer/venv/bin/python manage.py makemigrations
/home/itsuppus/svetorezerv/buyer/venv/bin/python manage.py migrate
#собрать статику
/home/itsuppus/svetorezerv/buyer/venv/bin/python manage.py collectstatic

cd /home/itsuppus/svetorezerv/buyer/textBlockClassifier/
docker rm -f /textBlockClassifier
docker build -t textblockclassifier .
docker run --restart=always -d -it -p 127.0.0.1:8000:8000 --name textBlockClassifier textblockclassifier
