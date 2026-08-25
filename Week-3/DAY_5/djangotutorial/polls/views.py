from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>Hello Paaji.</h1>")

def success(request):
    return HttpResponse("<h1>Success Page</h1>")

def detail(request, question_id):
    return HttpResponse(f"your are looking at Question {question_id}")

def results(requests, question_id):
    return HttpResponse(f"You are looking at the results of question: {question_id}")

def voting(requests, question_id):
    return HttpResponse(f"You are voting for question: {question_id}")
    