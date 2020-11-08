import re
from django.utils import timezone
from .keywords import *
from ..models import Message, Task, User
from .witai import WitEndpoint
from datetime import datetime, timedelta
from django.db.models import Q

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
        partern = re.match(f"^{keyword} ", text)
        if partern is not None:
            text = re.sub(f"^{keyword} ", "", text)
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
        "priority": 0,
        "status": 1,
        "version": "1"
    }

    entities = WitEndpoint().processing(text)["entities"]
    for key in entities:
        if key == "wit$location:location":
            location = [location_temp["body"] for location_temp in entities[key]]
            task["location"] = " | ".join(location)
        elif key == "wit$contact:contact":
            person = [person_temp["body"] for person_temp in entities[key]]
            task["people"] = " | ".join(person)
        elif key == "organization:organization":
            organization = [organization_temp["body"] for organization_temp in entities[key]]
            task["organization"] = " | ".join(organization)
        elif key == "priority:priority":
            priority = entities[key][0]["body"]
            task["priority"] = priority
        elif key == 'wit$datetime:start_datetime' or key == 'wit$datetime:datetime':
            if entities[key][0]['type'] == 'value':
                str_start_time = entities[key][0]['value']
                start_time = convert_stringto_datetime(str_start_time)
                end_time = add_time(start_time, entities[key][0]['grain'])
            elif entities[key][0]['type'] == 'interval':
                str_start_time = entities[key][0]['from']['value']
                start_time = convert_stringto_datetime(str_start_time)
                str_end_time = entities[key][0]['to']['value']
                end_time = convert_stringto_datetime(str_end_time)
            
            task["start"] = start_time
            task["expire"] = end_time

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
    #     requirement_type=1,
    #     user_id=user
    # )
    # mess.save()
    # task.messages.add(mess)

    task_object.messages.create(
        raw_text = task["text"], 
        create_location = "", 
        requirement_type = 1,
        user_id = user
    )
    
    context["task_list"].append(task)
    return context

def convert_stringto_datetime(str_time):
    str_time = str_time[:-10].replace('T', ' ')
    # print(str_time)
    
    # from django.forms.fields import DateTimeField
    # result = DateTimeField().clean(str_time)
    result = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    result = result.astimezone(timezone.get_current_timezone())
    print(result)
    return result

def add_time(this_time, duration):
    result = None
    if duration == 'hour':
        result = this_time + timedelta(hours=1)
    if duration == 'day':
        result = this_time + timedelta(days=1)
    if duration == 'week':
        result = this_time + timedelta(weeks=1)
    if duration == 'month':
        result = this_time + timedelta(months=1)
    if duration == 'year':
        result = this_time + timedelta(years=1)
    return result

def query(text, user_id):
    res = WitEndpoint().processing(text)
    entities = res['entities']
    print(entities)
    person_query = ''
    organization_query = ''
    location_query = ''
    date_query = ''
    start_time = None
    end_time = None
    for key in entities.keys():
        if key == 'wit$contact:contact':
            person_query = entities[key][0]['body']
        if key == 'organization:organization':
            organization_query = entities[key][0]['body']
        if key == 'wit$location:location':
            location_query = entities[key][0]['body']
        if key == 'wit$datetime:start_datetime' or key == 'wit$datetime:datetime':
            print('___type___')
            print(entities[key][0]['type'])
            if entities[key][0]['type'] == 'value':
                str_start_time = entities[key][0]['value']
                start_time = convert_stringto_datetime(str_start_time)
                end_time = add_time(start_time, entities[key][0]['grain'])
            elif entities[key][0]['type'] == 'interval':
                print(entities[key][0]['from'])
                str_start_time = entities[key][0]['from']['value']
                start_time = convert_stringto_datetime(str_start_time)
                str_end_time = entities[key][0]['to']['value']
                end_time = convert_stringto_datetime(str_end_time)
    print(start_time)
    print(end_time)
    print('*'*100)
    # print(type(date_query))
    if start_time is None or end_time is None:
        start_time = datetime(2020, 1, 1, 0, 0, 0).astimezone(timezone.get_current_timezone())
        end_time = datetime(2222, 1, 1, 0, 0, 0).astimezone(timezone.get_current_timezone())
    print(start_time)
    print(end_time)
    print(person_query)
    print(organization_query)
    print(location_query)
    current_time = datetime.now().astimezone(timezone.get_current_timezone())
    res = Task.objects.filter(user_id = user_id, person__contains=person_query, organization__contains = organization_query, location__contains=location_query, start_time__lt = start_time, expire_time__gt = end_time, status__in = [1 ,2]) | Task.objects.filter(user_id = user_id, person__contains=person_query, organization__contains = organization_query, location__contains=location_query, start_time__range=[start_time, end_time], status__in = [1, 2]) | Task.objects.filter(user_id = user_id, person__contains=person_query, organization__contains = organization_query, location__contains=location_query, expire_time__range=[start_time, end_time], status__in = [1, 2])
    # Q(start_time__range=[start_time, end_time]) | Q(expire_time__range=[start_time, end_time])
    
    print('___ query result ___')
    print(res)

    user = User.objects.get(id = user_id)
    mess = Message(
        raw_text=text, 
        create_location="", 
        requirement_type=3,
        user_id=user
    )
    mess.save()
    for task in res:
        task.messages.add(mess)

    ask_question = ''
    print(entities.keys())
    if key in entities.keys():
        if key == 'where:where' and organization_query != '':
            ask_question = 'organization:organization'
        elif key == 'where:where' and location_query != '':
            ask_question = 'wit$location:location'
            print(ask_question)
        if key == 'what:what':
            pass
        if key == 'when:when':
            ask_question = ['wit$datetime:datetime', 'wit$datetime:start_datetime']
            # ask_question = 'wit$datetime:start_datetime'


    print(ask_question)
    main_text = ''

    context = {'type': 'Query', 'old_task_list': [], 'task_list': [], 'text': text}
    for task in res:
        if ask_question != '':
            answers = WitEndpoint().processing(task.first_raw_text)
            print(answers['entities'])
            main_answer = None
            for aq in ask_question:
                if aq in answers['entities']:
                    main_answer = answers['entities'][aq]
            main_text = main_answer[0]['body']
        this_mess = {}
        this_mess['text'] = main_text + ' __ ' + task.first_raw_text
        this_mess['main_text'] = main_text
        this_mess['people'] = task.person
        this_mess['organization'] = task.organization
        this_mess['location'] = task.location
        this_mess['start'] = task.start_time
        this_mess['expire'] = task.expire_time
        this_mess['priority'] = task.priority
        this_mess['status'] = task.status
        this_mess['version'] = '1'
        context['task_list'].append(this_mess)
    return context
    
def classify(text, user_id):
    text = text.lower()
    for remind_word in REMIND_WORDS:
        if text.find(remind_word) != -1:
            return 'remind'
    
    for update_word in UPDATE_WORDS:
        if text.find(update_word) != -1:
            return 'update'
    
    return 'query'