from .keywords import *
from notes.models import Message, Task, User

def update(text, user_id):
    pass
    

def remind(text, usre_id, requirement_type):
    pass

def query(text, usre_id, requirement_type):
    pass

def classify(text, user_id):
    text = text.lower()
    for remind_word in REMIND_WORDS:
        if text.find(remind_word) != -1:
            return 'remind'
    
    for update_word in UPDATE_WORDS:
        if text.find(update) != -1:
            return 'update'
    
    return 'query'