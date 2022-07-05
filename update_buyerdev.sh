#!/bin/bash

#перейти в каталог с проектом
cd /
cd /home/itsuppus/svetorezerv/buyerdev/
git stash
git stash drop
git pull
#Удалить лишние миграции
sudo rm -f /home/itsuppus/svetorezerv/buyerdev/app/migrations/0001_initial.py

#создаём базу
sudo -u postgres psql -f init.sql
#восстанавливаем зависимости
/home/itsuppus/svetorezerv/buyerdev/venv/bin/python /home/itsuppus/svetorezerv/buyerdev/venv/bin/pip install -r ./requirements.txt
#обновить миграции
/home/itsuppus/svetorezerv/buyerdev/venv/bin/python manage.py makemigrations
/home/itsuppus/svetorezerv/buyerdev/venv/bin/python manage.py migrate
#собрать статику
/home/itsuppus/svetorezerv/buyerdev/venv/bin/python manage.py collectstatic

cd /home/itsuppus/svetorezerv/buyerdev/textBlockClassifier/
docker rm -f /textBlockClassifier
docker build -t textblockclassifier .
docker run -d --rm -it -p 8000:8000 --name textBlockClassifier textblockclassifier:latest

