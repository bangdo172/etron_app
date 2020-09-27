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
        print(question)
        
        context = {
            'answer_list': [
                {
                    "name": "Like a butterfly",
                    "type": "Boxing",
                    "hours": "9:00 AM - 11:00 AM",
                    "trainer": "Aaron Chapman",
                    "spots": "10"
                },
                {
                    "name": "Mind & Body",
                    "type": "Yoga",
                    "hours": "8:00 AM - 9:00 AM",
                    "trainer": "Adam Stewart",
                    "spots": "15"
                }
            ]
        }
        return response.Response(context, template_name='notes/index.html')