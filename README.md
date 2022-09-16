## Технологический стек
[![Django-app workflow](https://github.com/SoloMen88/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/SoloMen88/yamdb_final/actions/workflows/yamdb_workflow.yml)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

# CI/CD для проекта API YAMDB
Проект YaMDb собирает отзывы пользователей на различные произведения
В проекте реализован удобный Web API при помощи которого можно выполнять запросы к базе данных сайта.
Выполнен на Django Rest Framework c использование JSON token аутентификации библиотеки Simple JWT

Проект доступен по адрессу: http://solomen88.ddns.net/

## Требования:
- Python (3.7) 
- Django (2.2.16) 
- djangorestframework (3.12.4)
- simplejwt (4.7.2)
- Docker (20.10.17)

### Запуск приложения в контейнерах

Сначала нужно клонировать репозиторий и перейти в корневую папку:
```
git clone git@github.com:earlinn/infra_sp2.git
cd infra_sp2
```

Затем нужно перейти в папку infra_sp2/infra и создать в ней файл .env с 
переменными окружения, необходимыми для работы приложения.
```
cd infra/
```

Пример содержимого файла:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=key
DEBUG = False
ALLOWED_HOSTS = ['*']
```

Далее следует запустить docker-compose: 
```
docker-compose up -d
```
Будут созданы и запущены в фоновом режиме необходимые для работы приложения 
контейнеры (db, web, nginx).

Затем нужно внутри контейнера web выполнить миграции, создать 
суперпользователя и собрать статику:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```
После этого проект должен быть доступен по адресу http://localhost/. 

### Заполнение базы данных

Нужно зайти на на http://localhost/admin/, авторизоваться и внести записи 
в базу данных через админку.

Резервную копию базы данных можно создать командой
```
docker-compose exec web python manage.py dumpdata > fixtures.json 
```

### Остановка контейнеров

Для остановки работы приложения можно набрать в терминале команду Ctrl+C 
либо открыть второй терминал и воспользоваться командой
```
docker-compose stop 
```
Также можно запустить контейнеры без их создания заново командой
```
docker-compose start 
```

## Примеры запросов:
Получение списка всех категорий произведений:
```
http://127.0.0.1:8000/api/v1/categories/
```
Получение списка всех жанров:
```
http://127.0.0.1:8000/api/v1/genres/
```
Получение списка произведений, к которым пользователи пишут отзывы (определённый фильм, книга или песня):
```
http://127.0.0.1:8000/api/v1/titles/
```
Информация о конкретном произведении:
```
http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```
Получение списка всех отзывов:
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
Получение списка всех комментариев к отзыву:
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
Получить список всех пользователей:
```
http://127.0.0.1:8000/api/v1/users/
```
*Подробная документация API в формате redoc доступна по адресу:*
- http://127.0.0.1:8000/redoc/ 

### Работу выполнили:

- Эдуард Гафуров - (https://github.com/Edisson8)
- Станислав Кучеренко - (https://github.com/SoloMen88)
- Михаил Михайлов - (https://github.com/shogsy)
