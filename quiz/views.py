import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .models import Answer, Category, Question


# Create your views here.
def home(request):
    template_name = 'quiz/pages/home.html'
    categories = Category.objects.all()

    if request.GET.get('category'):
        return redirect(f'/quiz/?category={request.GET.get("category")}')

    context = {
        'categories': categories,
    }

    return render(request, template_name, context)


def quiz(request):
    category = request.GET.get('category')
    context = {
        'category': category,
    }
    return render(request, 'quiz/pages/quiz.html', context)


def get_quiz(request):
    try:
        questions = Question.objects.all()

        # Filtering questions by category if 'category' parameter is provided in the request
        # (Filtrando perguntas por categoria se o parâmetro 'category' for fornecido na solicitação)
        if request.GET.get('category'):
            category_name = request.GET.get('category')
            questions = questions.filter(
                category__name__icontains=category_name
            )

        # Converting queryset to list
        question_list = list(questions)

        # Shuffling the question list
        random.shuffle(question_list)

        data = []

        # Creating a dictionary for each question and its details
        # (Criando um dicionário para cada pergunta e seus detalhes)
        for question in question_list:
            data.append({
                'uuid': question.uuid,
                'question': question.question,
                'marks': question.marks,
                'category': question.category.name,
                'answers': question.get_answers(),
            })

        # returning JSON response
        # (retornando a resposta JSON)
        payload = {
            'status': True,
            'data': data,
        }

        return JsonResponse(payload)

    except Exception as e:
        print(e)
        return HttpResponse('Something went wrong!')
