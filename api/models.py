from django.db import models
from django.utils import timezone

class User(models.Model):
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Instructor', 'Instructor'),
    ]

    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # store hashed passwords
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.full_name} ({self.role})"

