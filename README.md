# FOODGRAM Продуктовый помощник
#### Описание
Сервис для обмена рецептами блюд, выбора понравившихся рецептов, отслеживания новинок понравившихся авторов, создания 
и скачивания списка покупок для похода в магазин за нужными ингредиентами

Сервер: http://angiolog.myftp.org/
Логин администратора: chuk@ya.ru
Пароль: 11111
#### Технологии
- Python 3.7
- Django 2.2.16
- Djangorestframework 3.12.4
#### Запуск проекта в dev-режиме
- Клонируйте репозиторий с помощью команды
````
git clone
````

- В папке infra создайте файл .env по следующему шаблону:
````
DEBUG=False(для отладки установить True)
SECRET_KEY=уникальный_секретный_ключ
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных - измените на свое
POSTGRES_USER=postgres # логин для подключения к базе данных - измените на свое
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```` 
 - Перейдите в папку infra
- Соберите контейнеры с помощью команды:
````
docker-compose up -d --build
````
- Выполните последовательно следующие команды:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

### Теперь проект доступен по адресу http://localhost/


### Авторы
Сергей Чукин