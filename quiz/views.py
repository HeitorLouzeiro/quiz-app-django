import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Answer, Category, Question


# Create your views here.
def home(request):
    return HttpResponse('Hello, Quiz App Django!')


def get_quiz(request):
    try:
        questions = list(Question.objects.all())
        data = []
        random.shuffle((questions))

        for question in questions:
            data.append({
                'question': question.question,
                'marks': question.marks,
                'category': question.category.name,
                'answers': question.get_answers(),
            })
        payload = {
            'status': True,
            'data': data,
        }

        return JsonResponse(payload)
    except Exception as e:
        print(e)
        return HttpResponse('Sommething went wrong!')
