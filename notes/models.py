from django.db import models
from multiselectfield import MultiSelectField

PRIORITY_CHOICES = (
    (0, 'Normality'),
    (1, 'Priority')
)

STATUS_CHOICES = (
    (0, 'Remove'),
    (1, 'Pending'),
    (2, 'Doing'),
    (3, 'Done')
)


GENDER_CHOICES = (
    (0, 'Not know'),
    (1, 'Female'),
    (2, 'Male'),
    (3, 'Other')
)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    raw_text = models.TextField()
    create_time = models.TimeField(auto_now=False, auto_now_add=True, null=True)
    last_edit_time = models.TimeField(auto_now=True, auto_now_add=False, null=True)
    start_time = models.TimeField(null = True)
    expire_time = models.TimeField(null = True)
    location = models.JSONField(null = True)
    person = models.JSONField(null = True)
    organize = models.JSONField(null = True)
    priority = MultiSelectField(choices = PRIORITY_CHOICES, max_choices = 1, null = True)
    status = MultiSelectField(choices = STATUS_CHOICES, max_choices = 1, null = True)
    user_id = models.IntegerField(null = True)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    gender = MultiSelectField(choices = GENDER_CHOICES, max_choices = 1)
    avatar = models.ImageField(upload_to=None)

