from django.db import models
from django.utils import timezone

class TaskState(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    customer_name = models.CharField(max_length=100)
    description = models.TextField()
    estimated_date = models.DateField()
    phone_number = models.CharField(max_length=15)
    work = models.CharField(max_length=100)
    created_date = models.DateField(default=timezone.now)  # Automatically set to today's date
    work_status = models.ForeignKey('TaskState', on_delete=models.SET_NULL, null=True)  # Link to TaskState model

    def __str__(self):
        return self.customer_name