import re
from ..models import Task

def update(text, usre_id, requirement_type):
    pass 

def remind(text, user_id):
    text = re.sub("^nhắc tôi ", "", text)
    
    pass

def query(text, usre_id, requirement_type):
    pass

def classify(text, user_id):
    pass