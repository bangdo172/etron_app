from django.contrib import admin

# Register your models here.
from .models import User, Message, Task

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Task)