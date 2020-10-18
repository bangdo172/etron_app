from django.db import models
from multiselectfield import MultiSelectField
import uuid
from datetime import datetime

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

REQUIREMENT_TYPE_CHOICES = (
    (0, 'Other'),
    (1, 'Remind'),
    (2, 'Update'),
    (3, 'Query')
)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    gender = MultiSelectField(choices = GENDER_CHOICES, max_choices = 1)
    avatar = models.ImageField(upload_to=None, null = True)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    raw_text = models.TextField(default='___ raw text ___')
    create_location = models.TextField(null = True, blank=True)
    requirement_type = MultiSelectField(choices = STATUS_CHOICES, max_choices = 1, null = True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return str(self.id) + ' _ ' + self.raw_text

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    first_raw_text = models.TextField(default='___ first your text ___')
    create_time = models.DateTimeField(default=datetime.now())
    last_edit_time = models.DateTimeField(default=datetime.now())
    start_time = models.DateTimeField(default=datetime.now())
    expire_time = models.DateTimeField(null = True, blank=True)
    location = models.TextField(null = True, blank=True)
    person = models.TextField(null = True, blank=True)
    organization = models.TextField(null = True, blank=True)
    priority = MultiSelectField(choices = PRIORITY_CHOICES, max_choices = 1, null = True)
    status = MultiSelectField(choices = STATUS_CHOICES, max_choices = 1, null = True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    messages = models.ManyToManyField(Message)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return str(self.id) + ' _ ' + self.first_raw_text
    