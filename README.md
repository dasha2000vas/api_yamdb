# API_YAMDB
<h5>YAMDB - это платформа для хранения информации о различных произведениях(книгах, музыке, фильмах), обмена отзывами и их обсуждения.</h5> 
<h5>API_YAMDB - интерфейс для взаимодействия c пользователем, позволяющий получать, создавать, удалять и изменять объекты.</h5>

## Как скачать и запустить проект:
1. Клонировать репозиторий и перейти в папку с ним:

```bash
git clone https://github.com/dasha2000vas/api_yamdb.git
cd api_yamdb
```

2. Создать и активировать виртуальное окружение:

```bash
python -m venv venv
source venv/Scripts/activate
```

3. Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

4. Перейти в папку с приложениями, выполнить миграции:

```bash
cd api_yamdb
python manage.py migrate
```

5. Запустить проект на локальном сервере:

```bash
python manage.py runserver
```

---
<br>

##Примеры запросов
1. Эндпоинт: http://127.0.0.1:8000/api/v1/auth/signup/. Метод запроса: POST

    При передаче следующих данных:

    * "email": "string" <text style="color:red">(required)</text>
    * "username": "string" <text style="color:red">(required)</text>

    Вы получите ответ о создании нового пользователя:

    * "email": "string"
    * "username": "string"

    Также на указанную почту будет оправлено письмо с кодом, необходимым для дальнейшей авторизации.

<br>

2. Эндпоинт: http://127.0.0.1:8000/api/v1/auth/token/. Метод запроса: POST

   При передаче имени зарегистрированного пользователя и кода из письма :

   * "email": "string" <text style="color:red">(required)</text>
   * "confirmation_code": "string" <text style="color:red">(required)</text>
  
   Вам в ответе будет отправлен токен, позволяющий авторизоваться:

   * "token": "string"

<br>

3. Эндпоинт: http://127.0.0.1:8000/api/v1/titles/. Метод запроса: GET

   В ответ вы получите список всех произведений, что имеются в базе данных. Опционально, можно параметризировать запрос фильтрацией и поиском по следующим полям: category(slug категории), genre(slug жанра), name(название), year(год выпуска).

<br>

4. Эндпоинт: http://127.0.0.1:8000/api/v1/titles/ Метод запроса: POST. Права доступа: администратор

    При передаче следующих данных:

    * "name": "string" <text style="color:red">(required)</text>
    * "year": "integer" <text style="color:red">(required)</text>
    * "description": "string"
    * "genre": "Array of strings" <text style="color:red">(required)</text>
    * "category": "string" <text style="color:red">(required)</text>

    В базу будет добавлено новое произведение и придет ответ в виде:
  
    * "id": "integer"
    * "name": "string"
    * "year": "integer"
    * "rating": "integer"
    * "description": "string"
    * "genre": "Array of objects"
    * "category": "object" 

<br>

5. Эндпоинт: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/. Метод запроса: GET

    При передаче следующих данных:

    * "title_id": "integer" <text style="color:red">(required)</text>
    * "review_id": "integer" <text style="color:red">(required)</text>
    
    Вернется ответ с информацией о конкретном отзыве, оставленном на указанное произведение:

    * "id": "integer"
    * "text": "string" <text style="color:red">(required)</text>
    * "author": "string"
    * "score": "integer" <text style="color:red">(required)</text>
    * "pub_date": "datetime"

<br>

6. Эндпоинт: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/. Метод запроса: PATCH. Права доступа: администратор, модератор, автор отзыва

    При передаче title_id и review_id со следующей информацией в теле запроса:

    * "text": "string" <text style="color:red">(required)</text>
    * "score": "integer" <text style="color:red">(required)</text>

    Соответствующий отзыв будет изменен и вернется ответ в таком виде:

    * "id": "integer"
    * "text": "string" <text style="color:red">(required)</text>
    * "author": "string"
    * "score": "integer" <text style="color:red">(required)</text>
    * "pub_date": "datetime"

<br>

> **Здесь приведены лишь некоторые запросы, доступные в проекте [API_YAMDB](#api_yamdb)**<br>
>Полный их список вы сможете увидеть, открыв документацию. Для этого необходимо [запустить проект на вашем компьютере](#как-скачать-и-запустить-проект) и перейти [по этому адресу](http://127.0.0.1:8000/redoc/).
