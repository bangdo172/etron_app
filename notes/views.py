from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import response
from rest_framework import generics

from .serializers import UserSerializer, GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class Index(generics.RetrieveAPIView):
    """
    A view that returns a templated HTML representation of a given user.
    """
    # queryset = User.objects.all()
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        question = request.GET.get('text') 
        if question is None:
            question = "What are you looking for?"
        
        context = {
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
            'question': {
                "text": question
            }
        }
        return response.Response(context, template_name='notes/index.html')