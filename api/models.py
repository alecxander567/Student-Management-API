from django.db import models
from django.utils import timezone

class User(models.Model):
    user_id = models.AutoField(primary_key=True)  # keep as primary key
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.full_name


class ClassInfo(models.Model):
    ClassID = models.AutoField(primary_key=True)
    ClassName = models.CharField(max_length=255)
    ClassCode = models.CharField(max_length=50, unique=True)
    Description = models.TextField()
    InstructorID = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='InstructorID',  # column name stays the same
        related_name='classes'
    )
    YearLevel = models.CharField(max_length=50)
    ScheduleDays = models.CharField(max_length=50)
    ScheduleTime = models.TimeField()
    DateCreated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "classes"

    def __str__(self):
        return self.ClassName


class Assignment(models.Model):
    AssignmentID = models.AutoField(primary_key=True)
    ClassID = models.ForeignKey(
        ClassInfo,
        on_delete=models.CASCADE,
        db_column='ClassID',
        related_name='assignments'
    )
    Title = models.CharField(max_length=255)
    Instructions = models.TextField()
    DatePosted = models.DateTimeField(default=timezone.now)
    DateOfSubmission = models.DateTimeField()

    class Meta:
        db_table = "assignments"

    def __str__(self):
        return self.Title


class Student(models.Model):
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    StudentID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    Department = models.CharField(max_length=100)
    YearLevel = models.PositiveIntegerField()

    ClassID = models.ForeignKey(
        'ClassInfo',
        on_delete=models.CASCADE,
        db_column='ClassID',
        related_name='students'
    )

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"
