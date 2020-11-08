from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import response
from rest_framework import generics

from .serializers import UserSerializer, GroupSerializer

from notes.nlp import *

class Index(generics.RetrieveAPIView):
    """
    A view that returns a templated HTML representation of a given user.
    """
    # queryset = User.objects.all()
    renderer_classes = [renderers.TemplateHTMLRenderer]

    @staticmethod
    def update(text, usre_id, requirement_type):
        pass 

    def get(self, request, *args, **kwargs):
        text = request.GET.get('text') 
        user_id = "1"
        if text is None:
            text = "What are you looking for?"
            return response.Response({"text":text}, template_name='notes/index.html')
        
        # requirement_type = nlp.classify(text, user_id)
        # if requirement_type == "remind":
        #     context = nlp.remind(text, user_id, requirement_type)

        # if requirement_type == "update":
        #     context = nlp.update(text, user_id, requirement_type)

        # if requirement_type == "query":
        #     context = nlp.query(text, user_id, requirement_type)
        
        context = {
            'type': "Remind",
            'old_task_list': [
                {
                    "text": "Like a butterfly",
                    "people": "Cinda",
                    "organization": "Baidu",
                    "location": "Hong Kong",
                    "start": "2:00 AM",
                    "expire": "11:00 AM",
                    "priority": "High",
                    "status": "Doing",
                    "version": "1"
                }
            ],
            'task_list': [
                {
                    "text": "Like a butterfly",
                    "people": "Aura",
                    "organization": "Apple Inc",
                    "location": "NY City",
                    "start": "9:00 AM",
                    "expire": "11:00 AM",
                    "priority": "High",
                    "status": "Doing",
                    "version": "2"
                },
                {
                    "text": "Mind & Body",
                    "people": "John",
                    "organization": "Google Inc",
                    "location": "Paris",
                    "start": "2:00 AM",
                    "expire": "5:00 AM",
                    "priority": "Low",
                    "status": "Pending",
                    "version": "1"
                }
            ],
            "text": text
        }

        return response.Response(context, template_name='notes/index.html')

# context = {
#     'type': "Remind",
#     'old_task_list': [
#         {
#             "text": "Like a butterfly",
#             "people": "Cinda",
#             "organization": "Baidu",
#             "location": "Hong Kong",
#             "start": "2:00 AM",
#             "expire": "11:00 AM",
#             "priority": "High",
#             "status": "Doing",
#             "version": "1"
#         }
#     ],
#     'task_list': [
#         {
#             "text": "Like a butterfly",
#             "people": "Aura",
#             "organization": "Apple Inc",
#             "location": "NY City",
#             "start": "9:00 AM",
#             "expire": "11:00 AM",
#             "priority": "High",
#             "status": "Doing",
#             "version": "2"
#         },
#         {
#             "text": "Mind & Body",
#             "people": "John",
#             "organization": "Google Inc",
#             "location": "Paris",
#             "start": "2:00 AM",
#             "expire": "5:00 AM",
#             "priority": "Low",
#             "status": "Pending",
#             "version": "1"
#         }
#     ],
#     "text": text
# }