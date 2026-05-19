# 🧑‍💻 FreelanceHub API

> ⚠️ **Учебный проект** — создан исключительно в образовательных целях. Все названия, концепции и реализация являются оригинальными. Любые совпадения с существующими платформами случайны и не нарушают авторских прав.

**FreelanceHub** — учебная backend-платформа для фриланс-биржи. Соединяет фрилансеров и заказчиков: клиенты создают проекты, фрилансеры подают предложения, система управляет рейтингами, отзывами и категориями.

🇷🇺 Русский · 🇬🇧 English · 🇰🇬 Кыргызча

---

## 🚀 Стек технологий

| Технология | Версия | Назначение |
|---|---|---|
| Python | 3.12 | Основной язык |
| Django | 5.2 | Web-фреймворк |
| Django REST Framework | latest | REST API |
| Simple JWT | latest | JWT-авторизация |
| Django Allauth | latest | OAuth (Google, GitHub) |
| Django Filters | latest | Фильтрация и поиск |
| drf-yasg | latest | Swagger документация |
| Modeltranslation | latest | Мультиязычность |
| SQLite / PostgreSQL | — | БД (dev / prod) |

---

## 👥 Роли пользователей

- **Client** — заказчик, создаёт проекты
- **Freelancer** — исполнитель, подаёт предложения
- **Admin** — администратор платформы

---

## 🔐 Авторизация

- JWT токены (`access`, `refresh`)
- Blacklist токенов при выходе (`/logout/`)
- OAuth через Google и GitHub (Django Allauth)
- Ролевая модель: `Freelancer`, `Client`, `Admin`

---

## 📦 Основные модели

| Модель | Описание |
|---|---|
| `UserProfile` | Расширенный пользователь: роль, био, навыки |
| `Skill` | Навыки фрилансера |
| `Project` | Проекты от заказчиков |
| `Offer` | Отклики от фрилансеров |
| `Review` | Отзывы между пользователями |
| `Category` | Категории проектов |
| `SocialLink` | Ссылки на соцсети пользователя |

---

## 📚 API эндпоинты

| Метод | URL | Описание |
|---|---|---|
| `POST` | `/register/` | Регистрация нового пользователя |
| `POST` | `/login/` | Вход, получение JWT токенов |
| `POST` | `/logout/` | Выход, blacklist refresh токена |
| `GET` | `/user/` | Список пользователей |
| `GET` | `/project/` | Список проектов |
| `GET` | `/offer/` | Список предложений |
| `GET` | `/docs/` | Swagger UI документация |

---

## ⚙️ Установка и запуск

```bash
# Клонировать репозиторий
git clone https://github.com/Omurbek000/freelancehub-api.git
cd freelancehub-api

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
python manage.py migrate

# Запустить сервер
python manage.py runserver
```

---

## 🛠️ Администрирование

- Доступна по адресу `/ru/admin/`
- Мультиязычность через `modeltranslation`
- Inline-модели: `SocialLink`, `Offer`
- Управление пользователями, проектами, отзывами

---

## 👨‍💻 Автор

**Aziat** — backend-разработчик, архитектор API, создатель FreelanceHub  
🔗 [github.com/Omurbek000/freelancehub-api](https://github.com/Omurbek000/freelancehub-api)

---

> 📌 Проект выполнен в учебных целях. Не предназначен для коммерческого использования.
