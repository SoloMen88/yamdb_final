![example workflow](https://github.com/SoloMen88/yamdb_final/actions/workflows/main.yml/badge.svg)
# YaMDb API
Проект YaMDb собирает отзывы пользователей на различные произведения
В проекте реализован удобный Web API при помощи которого можно выполнять запросы к базе данных сайта.
Выполнен на Django Rest Framework c использование JSON token аутентификации библиотеки Simple JWT

## Требования:
- Python (3.7) 
- Django (2.2.16) 
- djangorestframework (3.12.4)
- simplejwt (4.7.2)

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
