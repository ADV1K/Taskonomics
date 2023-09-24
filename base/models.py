import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    TIMEZONE_CHOICES = ((x, x) for x in pytz.all_timezones)
    timezone = models.CharField(
        max_length=32, default="Asia/Kolkata", choices=TIMEZONE_CHOICES, blank=False, null=False
    )


class Project(Base):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_owner")

    def __str__(self):
        return self.name


class Task(Base):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="current_project")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_creator")
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_assignee")
    reviewers = models.ManyToManyField(User, related_name="task_reviewers")
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
