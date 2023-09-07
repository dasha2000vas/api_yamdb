# API YAMDB

## 🔍Описание:
<h4>Проект YAMDB собирает отзывы пользователей на произведения. Сами произведения в проекте не хранятся, здесь нельзя посмотреть фильм или послушать музыку.</h4>
<h4>

<mark style="color:#00a6ff"><u>[API YAMDB*](#api-yamdb)</u> - интерфейс для взаимодействия c пользователем, позволяющий получать, создавать, удалять и изменять объекты в базе данных <u>[проекта](#описание)</u>.</mark>
</h4>

![LOGOTYPE](https://keenethics.com/wp-content/uploads/2022/01/rest-api-1.svg "img.png")

---

## 💡Как скачать и запустить проект:
1. **Клонировать репозиторий и перейти в папку с ним:**

```bash
git clone https://github.com/dasha2000vas/api_yamdb.git
cd api_yamdb
```

2. **Создать и активировать виртуальное окружение:**

```bash
python -m venv venv
source venv/Scripts/activate
```

3. **Установить зависимости из файла requirements.txt:**

```bash
pip install -r requirements.txt
```

4. **Перейти в папку с приложениями, выполнить миграции:**

```bash
cd api_yamdb
python manage.py migrate
```

5. **Запустить проект на локальном сервере:**

```bash
python manage.py runserver
```

---

## ▶️Примеры запросов:
>Перед запуском учтите условия, описанные в [примечании⬇️](#примечание)...
1. **Эндпоинт: http://127.0.0.1:8000/api/v1/auth/signup/. Метод запроса: POST<br>Права доступа: Доступно без токена**

    При передаче следующих данных:

    * "email": "string" <mark>(required)</mark>,
    * "username": "string" <mark>(required)</mark>

    Вы получите ответ о создании нового пользователя:

    * "email": "string",
    * "username": "string"

    >*Также, на указанную почту будет оправлено письмо с кодом, необходимым для дальнейшей авторизации.*

<br>

2. **Эндпоинт: http://127.0.0.1:8000/api/v1/auth/token/. Метод запроса: POST<br>Права доступа: Доступно без токена**

   При передаче имени зарегистрированного пользователя и кода из письма:

   * "email": "string" <mark>(required)</mark>,
   * "confirmation_code": "string" <mark>(required)</mark>
  
   Вам в ответе будет отправлен ***JWT Token***, позволяющий авторизоваться:

   * "token": "string"

<br>

3. **Эндпоинт: http://127.0.0.1:8000/api/v1/titles/. Метод запроса: GET<br>Права доступа: Доступно без токена**

   В ответ вы получите список всех произведений, что имеются в базе данных. Опционально, можно параметризировать запрос фильтрацией и поиском по следующим полям: category (slug категории), genre (slug жанра), name (название), year(год выпуска).

<br>

4. **Эндпоинт: http://127.0.0.1:8000/api/v1/titles/ Метод запроса: POST.<br> Права доступа: Администратор**

    При передаче следующих данных **в теле запроса**:

    * "name": "string" <mark>(required)</mark>,
    * "year": "integer" <mark>(required)</mark>,
    * "description": "string",
    * "genre": "array of strings" <mark>(required)</mark>,
    * "category": "string" <mark>(required)</mark>
    
    В базу будет добавлено новое произведение и придет ответ в виде:
  
    * "id": "integer",
    * "name": "string",
    * "year": "integer",
    * "rating": "integer",
    * "description": "string",
    * "genre": "Array of objects",
    * "category": "object" 

<br>

5. **Эндпоинт: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/. Метод запроса: GET<br>Права доступа: Доступно без токена**

    При передаче следующих данных **в параметрах запроса:**

    * "title_id": "integer" <mark>(required)</mark>,
    * "review_id": "integer" <mark>(required)</mark>
    
    Вернется ответ с информацией о конкретном отзыве, оставленном на указанное произведение:

    * "id": "integer",
    * "text": "string" <mark>(required)</mark>,
    * "author": "string",
    * "score": "integer" <mark>(required)</mark>,
    * "pub_date": "datetime"

<br>

6. **Эндпоинт: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/. Метод запроса: PATCH.<br>Права доступа: Администратор, Модератор, Автор отзыва**

    При передаче следующей информации **в теле запроса:**

    * "text": "string" <mark>(required)</mark>,
    * "score": "integer" <mark>(required)</mark>

    Соответствующий отзыв будет изменен и вернется ответ в таком виде:

    * "id": "integer",
    * "text": "string" <mark>(required)</mark>,
    * "author": "string",
    * "score": "integer" <mark>(required)</mark>,
    * "pub_date": "datetime"


---
### Примечание:
> **В данном руководстве приведены лишь некоторые запросы, доступные в проекте [API YAMDB](#api_yamdb)**.
>>Чтобы увидеть полный список возможных запросов (эндпоинтов), Вы можете открыть полноценную документацию: для этого необходимо [запустить проект на вашем компьютере](#как-скачать-и-запустить-проект) и перейти [по этому адресу](http://127.0.0.1:8000/redoc/).
