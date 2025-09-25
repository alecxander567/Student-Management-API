from django.db import models
from django.utils import timezone

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

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
        db_column='InstructorID'
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
    ClassID = models.ForeignKey('ClassInfo', on_delete=models.CASCADE, db_column='ClassID')
    Title = models.CharField(max_length=255)
    Instructions = models.TextField()
    DatePosted = models.DateTimeField(default=timezone.now)
    DateOfSubmission = models.DateTimeField()

    class Meta:
        db_table = "assignments"

    def __str__(self):
        return self.Title

class Activity(models.Model):
    ActivityID = models.AutoField(primary_key=True)
    ClassID = models.ForeignKey('ClassInfo', on_delete=models.CASCADE, db_column='ClassID')
    Title = models.CharField(max_length=255)
    Instructions = models.TextField()
    DatePosted = models.DateTimeField(default=timezone.now)
    DateOfSubmission = models.DateTimeField()

    class Meta:
        db_table = "activities"

    def __str__(self):
        return self.Title