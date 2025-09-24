from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Skill(models.Model):
    skill_name = models.CharField(max_length=100)

    def __str__(self):
        return self.skill_name


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ("Freelancer", "Freelancer"),
        ("client", "client"),
        ("admin", "admin"),
    )
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(region="KG", null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True, null=True)

    def __str__(self):
        return f"{ self.first_name } { self.last_name } {self.role}"


class SocialLink(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )
    platform = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return f"{self.platform}: {self.url}"


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Project(models.Model):
    STATUS_CHOICES = (
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=7, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill, blank=True, null=True)
    client = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="projects"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Offer(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    freelancer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )
    message = models.TextField()
    proposed_budget = models.DecimalField(max_digits=7, decimal_places=2)
    proposed_deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    reviewer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE, related_name='reviews'
    )
    target = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE, related_name='target')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
