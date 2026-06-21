🌐 FreelanceHub API — Платформа для фриланс‑проекта

⚠️ Учебный проект.  
Создан исключительно в образовательных целях. Все совпадения случайны.

🏆 О проекте
FreelanceHub API — это backend‑платформа, которая соединяет заказчиков и фрилансеров.
Заказчики публикуют проекты, фрилансеры откликаются, а после завершения — обмениваются отзывами и рейтингами.

| Технология | Версия | Описание |
| --- | --- | --- |
| Python | 3.12 | Язык разработки |
| Django | 5.2 | Backend‑фреймворк |
| DRF | 3.16 | REST API |
| SimpleJWT | — | JWT‑аутентификация |
| Allauth | — | GitHub/Google OAuth |
| Swagger | — | Автодокументация |
| Modeltranslation | — | Мультиязычность |
| Django‑filter | — | Фильтрация |
| DRF Throttling | — | Rate limiting |

🧩 Модели данных
UserProfile — пользователь (Freelancer / Client / Admin)

Skill — навыки

Category — категории проектов

Project — проект заказчика

Offer — предложение фрилансера

Review — отзыв и рейтинг

SocialLink — соц. ссылки

🔗 API Эндпоинты
🔐 Аутентификация
POST /register/ — регистрация

POST /login/ — JWT‑логин

POST /logout/ — выход

👤 Пользователи
GET /user/ — список

GET /user/<id>/ — профиль

GET /users-simple/ — CRUD

📁 Проекты
GET /projects/ — CRUD

GET /project/ — публичный список

GET /project/<id>/ — детали

🏷 Категории
GET /categories/ — CRUD

💼 Предложения
GET /offers/ — CRUD

GET /offer/ — публичный список

GET /offer/<id>/ — детали

⭐ Отзывы
GET /reviews/ — CRUD

📘 Документация
GET /docs/ — Swagger UI

🛠 Админ‑панель
GET /admin/ — Django Admin

| Роль | Описание |
| --- | --- |
| **Client** | создаёт проекты |
| **Freelancer** | подаёт предложения |
| **Admin** | управляет платформой |

⏳ Ограничение запросов (Rate Limiting)
Анонимные: 100/час

Авторизованные: 1000/час

Логин: 5/мин

🔑 JWT‑токены
Access: 30 минут

Refresh: 7 дней

Формат: Authorization: Bearer <access_token>

# 1. Установка зависимостей
pip install -r requirements.txt

# 2. Создание .env
SECRET_KEY=your-secret-key

# 3. Миграции
python manage.py migrate

# 4. Создание суперпользователя
python manage.py createsuperuser

# 5. Запуск сервера
python manage.py runserver
          
🔗 Полезные ссылки
Swagger: http://127.0.0.1:8000/docs/

Admin: http://127.0.0.1:8000/admin/

freelancehub/
├── freelancehub/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── freelance/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   ├── filters.py
│   ├── pagination.py
│   ├── translation.py
│   ├── admin.py
│   └── migrations/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── .env
└── README.py
