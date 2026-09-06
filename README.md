<div align="center">

# 💼 FreelanceHub API

<p>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/DRF-3.16-FF1709?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=jsonwebtokens&logoColor=white"/>
  <img src="https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black"/>
</p>

**Backend для фриланс-биржи — клиенты создают проекты, фрилансеры откликаются**

`Skill → UserProfile → Category → Project → Offer → Review`

[📖 Swagger](http://127.0.0.1:8000/docs/) • [🛠️ Админка](http://127.0.0.1:8000/admin/) • `GET /health/`

</div>

---

## ✨ Что умеет

| | Возможность | Детали |
|---|---|---|
| 👤 | **Роли** | `Freelancer` / `Client` / `Admin` (`UserProfile` + `AbstractUser`) |
| 🛠️ | **Навыки** | `Skill` (Python, JS, React...), `ManyToMany` к профилю |
| 📂 | **Категории** | `Category` (веб-разработка, дизайн...) |
| 📋 | **Проекты** | `Project` (бюджет, дедлайн, статус `open`/`closed`) |
| 💬 | **Отклики** | `Offer` (цена, срок, сообщение), один на проект |
| ⭐ | **Отзывы** | `Review` (звезды, текст) после завершения |
| 🔗 | **Соцсети** | `SocialLink` (GitHub, Telegram) |
| 🔐 | **Авторизация** | `JWT` + `allauth` (GitHub, Google) |
| 🌐 | **Мультиязык** | `modeltranslation` `ru/en/ky` |
| 📄 | **Пагинация** | `PageNumberPagination` 10 |

---

## 🧱 Стек

| | Технология | Зачем | Где |
|---|---:|---|---|
| 🐍 | **Django 5.2** | Модели, админка | `freelancehub/freelance/models.py:1` |
| 🧩 | **DRF 3.16** | Сериализаторы, `ViewSet` | `serializers.py` |
| 🔐 | **SimpleJWT + allauth** | `JWT` + `OAuth` GitHub/Google | `views.py` |
| 🌐 | **modeltranslation** | `ru/en/ky` админка | `translation.py` |
| 🔎 | **django-filter** | `ProjectFilter` | `filters.py` |
| 📄 | **drf-yasg** | Swagger `/docs/` | `urls.py` |
| 🗄️ | **SQLite** | `dev` (Postgres на проде) | `settings.py` |

---

## 📦 Структура

```
freelancehub-api/
├── freelancehub/
│   ├── freelancehub/       # settings, urls, wsgi
│   └── freelance/
│       ├── models.py       # Skill, UserProfile, Category, Project, Offer, Review
│       ├── serializers.py  # ProjectSerializer, OfferSerializer
│       ├── views.py        # ProjectViewSet, OfferViewSet
│       ├── urls.py         # router + auth
│       ├── filters.py      # ProjectFilter
│       └── tests.py
├── requirements.txt
└── manage.py
```

---

## 🚀 Быстрый старт

<details>
<summary><b>1️⃣ Клонировать</b></summary>

```powershell
git clone https://github.com/Omurbek000/freelancehub-api.git
cd freelancehub-api
```

</details>

<details>
<summary><b>2️⃣ Зависимости</b></summary>

```powershell
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # или создай .env
```

`requirements.txt`: `Django`, `djangorestframework`, `djangorestframework-simplejwt`, `django-allauth`, `django-modeltranslation`, `drf-yasg`

</details>

<details>
<summary><b>3️⃣ .env</b></summary>

```ini
SECRET_KEY=your-secret
DEBUG=True
ALLOWED_HOSTS=*
POSTGRES_DB=freelancehub
POSTGRES_USER=freelancehub
POSTGRES_PASSWORD=1234
```

</details>

<details>
<summary><b>4️⃣ Миграции + админ</b></summary>

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# http://127.0.0.1:8000/admin/
# http://127.0.0.1:8000/docs/
```

</details>

<details>
<summary><b>5️⃣ Проверить</b></summary>

```powershell
curl -X POST http://127.0.0.1:8000/auth/register/ -H "Content-Type: application/json" -d "{\"username\":\"test\",\"password\":\"123456\"}"
curl -X POST http://127.0.0.1:8000/auth/login/ -d "{\"username\":\"test\",\"password\":\"123456\"}"
```

</details>

---

## 🔗 API

| Метод | Endpoint | Описание |
|---|---|---|
| POST | `/auth/register/` | регистрация |
| POST | `/auth/login/` | JWT |
| GET | `/skills/` | навыки |
| GET | `/categories/` | категории |
| GET | `/projects/` | проекты `?category=&skill=` |
| POST | `/projects/` | создать (Client) |
| POST | `/projects/{id}/offers/` | отклик (Freelancer) |
| GET | `/offers/` | мои отклики |
| POST | `/reviews/` | отзыв |

---

## 📝 Заметки

- `UserProfile` расширяет `AbstractUser`, `PhoneNumberField(region="KG")`
- `Offer` — один на проект от фрилансера (`unique_together`)
- Комментарии в коде — на русском, стиль `user-backend-style`

---

<div align="center">

**FreelanceHub** · Django 5.2 · DRF · 2026

</div>
