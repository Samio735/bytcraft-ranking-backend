from django.db import models
from datetime import date
# Create your models here.
DEPARTMENT_CHOICES = (
    ('development', 'Development'),
    ('design', 'Design'),
    ('communication', 'Communication'),
    ('relex-logistics', 'Relex and logistics'),
    ("multimedia", "Multimedia"),
)


class Member(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    department = models.CharField(choices=DEPARTMENT_CHOICES, null=True, blank=True, max_length=100)
    points = models.IntegerField(default=0)


ACTIVITY_TYPE_CHOICES = (
    ('meet', 'Meeting'),
    ("task", "Task"),
    ("part", "event participation"),
    ("organ", "event organization"),
)

ACTIVITY_STATUS_CHOICES = (
    ("active", "Active"),
    ("finished", "Finished"),
)

IMPORTANCE_CHOICES = (
    ("training", "Training"),
    ("important", "Important"),
)

TIME_CHOICES = (
    ("quick", "Quick"),
    ("takes-time", "Takes time"),
    ("ongoing", "Ongoing"),
)

class Activities(models.Model):
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)
    type = models.CharField(choices=ACTIVITY_TYPE_CHOICES, max_length=100)
    date_created = models.DateField(default=date.today)
    status = models.CharField(choices=ACTIVITY_STATUS_CHOICES, max_length=10,default="active")
    members = models.ManyToManyField(Member, related_name="activities",blank=True)
    department = models.CharField(choices=DEPARTMENT_CHOICES, max_length=100)
    importance = models.CharField(max_length=100, choices=IMPORTANCE_CHOICES, default="training")
    time = models.CharField(max_length=100, choices=TIME_CHOICES, default="quick")
