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
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.full_name} ({self.role})"

class ClassInfo(models.Model):
    ClassID = models.AutoField(primary_key=True)
    ClassName = models.CharField(max_length=255)
    ClassCode = models.CharField(max_length=50, unique=True)
    Description = models.TextField()
    InstructorID = models.IntegerField()
    YearLevel = models.CharField(max_length=50)
    ScheduleDays = models.CharField(max_length=50)
    ScheduleTime = models.TimeField()
    DateCreated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "classes"

