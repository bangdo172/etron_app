import re
from datetime import datetime
from .keywords import *
from ..models import Message, Task, User
from .witai import WitEndpoint
from datetime import datetime, timedelta

def update(text, user_id):
    for keyword in UPDATE_WORDS:
        partern = re.match(f"^{keyword} ", text.lower())
        if partern is not None:
            text = re.sub(f"^{keyword} ", "", text.lower())
            update_word = text
            break
        
    context = {
        'type': "Update",
        'task_list': [],
        'old_task_list': [],
        "text": text
    }

    entities = WitEndpoint().processing(text)

    for key in entities:
        if key == "wit$location:location":
            location = [location_temp["body"] for location_temp in entities[key]]
        elif key == "wit$contact:contact":
            person = [person_temp["body"] for person_temp in entities[key]]
        elif key == "organization:organization":
            organization = [organization_temp["body"] for organization_temp in entities[key]]
    
    if person is None:
        person = []
    if location is None:
        location = []
    if organization is None:
        organization = []
        
    task_update_list = Task.objects.filter(
        user_id = user_id, 
        person__contains=person[0], 
        organization__contains = organization[0], 
        location__contains=location[0]
    )    

    if update_word in CANCEL_WORDS:
        for task_object in task_update_list:
            task_old = {
                "text": task_object.first_raw_text,
                "people": task_object.person,
                "organization": task_object.organization,
                "location": task_object.location,
                "start": task_object.start_time,
                "expire": task_object.expire_time,
                "priority": task_object.priority,
                "status": task_object.status,
                "version": "1"
            }
            task_object.status = "Remove"
            task_object.last_edit_time = str(datetime.now())
            task_object.save()

            task_new = {
                "text": task_object.first_raw_text,
                "people": task_object.person,
                "organization": task_object.organization,
                "location": task_object.location,
                "start": task_object.start_time,
                "expire": task_object.expire_time,
                "priority": task_object.priority,
                "status": task_object.status,
                "version": "2"
            }

            context["task_list"].append(task_new)
            context["old_task_list"].append(task_old)
            
    elif update_word in CHECK_WORDS:
        for task_object in task_update_list:
            task_old = {
                "text": task_object.first_raw_text,
                "people": task_object.person,
                "organization": task_object.organization,
                "location": task_object.location,
                "start": task_object.start_time,
                "expire": task_object.expire_time,
                "priority": task_object.priority,
                "status": task_object.status,
                "version": "1"
            }
            task_object.status = "Done"
            task_object.last_edit_time = str(datetime.now())
            task_object.save()

            task_new = {
                "text": task_object.first_raw_text,
                "people": task_object.person,
                "organization": task_object.organization,
                "location": task_object.location,
                "start": task_object.start_time,
                "expire": task_object.expire_time,
                "priority": task_object.priority,
                "status": task_object.status,
                "version": "2"
            }

            context["task_list"].append(task_new)
            context["old_task_list"].append(task_old)
        
    elif update_word in CHECK_WORDS:
        if len(task_update_list) > 0:
            task_object = task_update_list[0]
            task_old = {
                "text": task_object.first_raw_text,
                "people": task_object.person,
                "organization": task_object.organization,
                "location": task_object.location,
                "start": task_object.start_time,
                "expire": task_object.expire_time,
                "priority": task_object.priority,
                "status": task_object.status,
                "version": "1"
            }

            if len(person) > 0:
                task_object.person = person[0]
            if len(organization) > 0:
                task_object.organization = organization[0]
            if len(location) > 0:
                task_object.location = location[0]
            
            task_object.last_edit_time = str(datetime.now())
            task_object.save()

            task_new = {
                "text": task_object.first_raw_text,
                "people": task_object.person,
                "organization": task_object.organization,
                "location": task_object.location,
                "start": task_object.start_time,
                "expire": task_object.expire_time,
                "priority": task_object.priority,
                "status": task_object.status,
                "version": "2"
            }

            context["task_list"].append(task_new)
            context["old_task_list"].append(task_old)

    return context

def remind(text, user_id):
    for keyword in REMIND_WORDS:
        partern = re.match(f"^{keyword} ", text.lower())
        if partern is not None:
            text = re.sub(f"^{keyword} ", "", text.lower())
            break

    context = {
        'type': "Remind",
        'task_list': [],
        "text": text
    }

    now = str(datetime.now()).replace(" ", "T") + "+07:00"

    task = {
        "text": text,
        "people": "",
        "organization": "",
        "location": "",
        "start": now,
        "expire": now,
        "priority": "Normality",
        "status": "Pending",
        "version": "1"
    }

    entities = WitEndpoint().processing(text)["entities"]
    for key in entities:
        if key == "wit$location:location":
            location = [location_temp["body"] for location_temp in entities[key]]
            task["location"] = " | ".join(location)
        elif key == "wit$contact:contact":
            person = [person_temp["body"] for person_temp in entities[key]]
            task["person"] = " | ".join(person)
        elif key == "organization:organization":
            organization = [organization_temp["body"] for organization_temp in entities[key]]
            task["organization"] = " | ".join(organization)
        elif key == "priority:priority":
            priority = entities[key][0]["body"]
            task["priority"] = priority
        elif key == "wit$datetime:start_datetime":
            start_time = entities[key][0]["value"]
            task["start"] = start_time
        elif key == "wit$datetime:datetime":
            expire_time = entities[key][0]["value"]
            task["start"] = expire_time

    # Update Priority and Status Here
    user = User.objects.get(id = user_id)

    task_object = Task(
        first_raw_text = task["text"],
        start_time = task["start"],
        expire_time = task["expire"],
        location = task["location"],
        person = task["people"],
        organization = task["organization"],
        priority = task["priority"],
        status = task["status"],
        user_id = user
    )
    task_object.save()

    # mess = Message(
    #     raw_text=task["text"], 
    #     create_location="", 
    #     requirement_type="remind",
    #     user_id=user_id
    # )
    # mess.save()
    # task.messages.add(mess)

    task_object.messages.create(
        raw_text = task["text"], 
        create_location = "", 
        requirement_type = "remind",
        user_id = user
    )
    
    context = context["task_list"].append(task)
    return context

def query(text, user_id):

    res = WitEndpoint().processing(text)
    entities = res['entities']
    print(entities)
    person_query = ''
    organization_query = ''
    location_query = ''
    date_query = ''
    start_time = ''
    end_time = ''
    for key in entities.keys():
        if key == 'wit$contact:contact':
            person_query = entities[key][0]['value']
        if key == 'organization:organization':
            organization_query = entities[key][0]['value']
        if key == 'wit$location:location':
            location_query = entities[key][0]['value']
        if key == 'wit$datetime:start_datetime':
            if entities[key][0]['type'] == 'value':
                print('__value__')
                str_start_time = entities[key][0]['value']
                print(str_start_time)
                start_time = datetime.strptime(date_query, "%Y-%m-%dT%H:%M:%S.%f+%Z")
                print('__str_start_time__')
            elif entities[key][0]['type'] == 'internal':
                print('__internal__')
                # start_time = entities[key][0]['from']

    print('*'*100)
    # print(type(date_query))
    if date_query != '':
        print(date_query)
        _start_time = datetime.strptime(date_query, "%Y-%m-%dT%H:%M:%S.%f+%Z")
        print(_start_time)
        _end_time = ''

    res = Task.objects.filter(user_id = user_id, person__contains=person_query, organization__contains = organization_query, location__contains=location_query)
    
    ask_question = ''
    if key in entities.keys():
        if key == 'where:where' and organization_query != '':
            ask_question = 'organization:organization'
        elif key == 'where:where' and location_query != '':
            ask_question = 'wit$location:location'
            print(ask_question)
        if key == 'what:what':
            pass
        if key == 'when:when':
            ask_question = 'wit$datetime:datetime'

    print(ask_question)
    main_text = ''
    if ask_question != '':
        answers = WitEndpoint().processing(res[0].first_raw_text)
        print(answers['entities'])
        main_answer = answers['entities'][ask_question]
        print('-'*100)
        print(main_answer)
        main_text = main_answer[0]['body']
        print('')
        print(main_text)
    
    return res, main_text
    
def classify(text, user_id):
    text = text.lower()
    for remind_word in REMIND_WORDS:
        if text.find(remind_word) != -1:
            return 'remind'
    
    for update_word in UPDATE_WORDS:
        if text.find(update) != -1:
            return 'update'
    
    return 'query'