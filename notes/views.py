from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {'latest_question_list': [1, 2, 3]}
    return render(request, 'notes/index.html', context)

    # return HttpResponse("Hello, world. You're at the polls index.")
