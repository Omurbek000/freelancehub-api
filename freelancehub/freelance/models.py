"""
Модели базы данных для фриланс-платформы FreelanceHub.

Модели:
- Skill — навыки (Python, JavaScript, и т.д.)
- UserProfile — кастомный пользователь (расширяет AbstractUser)
- SocialLink — социальные ссылки пользователя (GitHub, Telegram)
- Category — категории проектов (Веб-разработка, Дизайн)
- Project — проекты, создаваемые заказчиками
- Offer — предложения от фрилансеров на проекты
- Review — отзывы/рейтинги после завершения проекта
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Skill(models.Model):
    """
    Модель навыков/технологий.
    Используется для тегирования пользователей и проектов.
    Пример: Python, JavaScript, React, Photoshop
    """
    skill_name = models.CharField(max_length=100)

    def __str__(self):
        return self.skill_name


class UserProfile(AbstractUser):
    """
    Кастомная модель пользователя (расширяет стандартную Django User).
    Добавляет: роль (Freelancer/Client/Admin), телефон, биографию, аватар, навыки.

    Роли:
    - Freelancer — исполнитель, выполняет проекты
    - client — заказчик, создаёт проекты
    - admin — администратор платформы
    """
    ROLE_CHOICES = (
        ("Freelancer", "Freelancer"),
        ("client", "client"),
        ("admin", "admin"),
    )
    email = models.EmailField(unique=True)                          # Уникальный email
    phone_number = PhoneNumberField(region="KG", null=True, blank=True)  # Номер телефона (Кыргызстан по умолчанию)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)    # Роль пользователя
    bio = models.TextField(blank=True, null=True)                   # Биография / описание
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)  # Аватар
    skills = models.ManyToManyField(Skill)                          # Навыки (M2M)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class SocialLink(models.Model):
    """
    Социальные ссылки пользователя.
    Пример: GitHub — https://github.com/username
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Владелец ссылки
    platform = models.CharField(max_length=50)                       # Платформа (GitHub, Telegram, и т.д.)
    url = models.URLField(blank=True, null=True)                     # Ссылка

    def __str__(self):
        return f"{self.platform}: {self.url}"


class Category(models.Model):
    """
    Категории проектов для классификации.
    Пример: Веб-разработка, Мобильная разработка, Дизайн
    """
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Project(models.Model):
    """
    Проект, создаваемый заказчиком (client).
    Содержит: название, описание, бюджет, дедлайн, статус, категорию, навыки.

    Статусы:
    - open — проект открыт для предложений
    - in_progress — проект в работе
    - completed — проект завершён
    - cancelled — проект отменён
    """
    STATUS_CHOICES = (
        ("open", "Open"),            # Открыт для предложений
        ("in_progress", "In Progress"),  # В работе
        ("completed", "Completed"),  # Завершён
        ("cancelled", "Cancelled"),  # Отменён
    )
    title = models.CharField(max_length=255)                         # Название проекта
    description = models.TextField()                                 # Описание проекта
    budget = models.DecimalField(max_digits=7, decimal_places=2)    # Бюджет (до 99999.99)
    deadline = models.DateField()                                    # Дедлайн
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")  # Статус
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="projects_category")  # Категория
    skills = models.ManyToManyField(Skill)                           # Необходимые навыки (M2M)
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="projects_client")  # Заказчик
    created_at = models.DateTimeField(auto_now_add=True)             # Дата создания (автоматически)

    def __str__(self):
        return self.title


class Offer(models.Model):
    """
    Предложение (отклик) от фрилансера на проект.
    Содержит: сообщение, предложенный бюджет, предложенный дедлайн.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='offer_project')  # Проект
    freelancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='offer_freelancer')  # Фрилансер
    message = models.TextField()                                     # Сообщение/описание предложения
    proposed_budget = models.DecimalField(max_digits=7, decimal_places=2)  # Предложенный бюджет
    proposed_deadline = models.DateField()                            # Предложенный дедлайн
    created_at = models.DateTimeField(auto_now_add=True)             # Дата создания

    def __str__(self):
        return f"Offer by {self.freelancer} for {self.project}"


class Review(models.Model):
    """
    Отзыв/рейтинг одного пользователя на другого после проекта.
    reviewer → target (от кого → кому)
    Рейтинг от 1 до 5.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='review_project')  # Проект
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')   # Кто оставил отзыв
    target = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='review_target')  # Кому отзыв
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]  # Рейтинг от 1 до 5
    )
    comment = models.TextField()                                     # Текст отзыва
    created_at = models.DateTimeField(auto_now_add=True)             # Дата создания

    def __str__(self):
        return f"Review by {self.reviewer} → {self.target} ({self.rating}/5)"
