#!/bin/bash
#перейти в каталог с проектом
cd /home/itsuppus/svetorezerv/buyer/
#выключить все контейнеры
docker-compose down -v
#Удалить все контейнеры
docker system prune -a
#Удалить все разделы
docker volume prune
# update code
git pull
#Удалить лишние миграции
sudo rm -f /home/itsuppus/svetorezerv/buyer/app/migrations/0001_initial.py
# собрать образ
docker-compose up -d --build
#обновить миграции
docker-compose exec app python manage.py makemigrations
docker-compose exec app python manage.py migrate
#собрать статику
docker-compose exec app python manage.py collectstatic