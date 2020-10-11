import re
from ..models import Task
from .keywords import *
from notes.models import Message, Task, User

def update(text, user_id):
    pass

def remind(text, user_id):
    text = re.sub("^nhắc tôi ", "", text)

    pass

def query(text, usre_id, requirement_type):
    pass

def classify(text, user_id):
    pass