from django.http import HttpResponse
from . models import Question
from django.shortcuts import render


# def index(request):
#     return HttpResponse("<h1>Hello Paaji.</h1>")

# def success(request):
#     return HttpResponse("<h1>Success Page</h1>")

# def detail(request, question_id):
#     return HttpResponse(f"your are looking at Question {question_id}")

# def results(requests, question_id):
#     return HttpResponse(f"You are looking at the results of question: {question_id}")

# def voting(requests, question_id):
#     return HttpResponse(f"You are voting for question: {question_id}")

def index(request):
    latest_question_list = Question.objects.order_by("pub_date")[:5]
    context = {"latest_question_list" : latest_question_list}
    return render(request, "polls/index.html", context)
