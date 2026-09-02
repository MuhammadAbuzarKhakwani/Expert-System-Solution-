from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


def success(request):
    return HttpResponse("<h1>Success Page</h1>")


def voting(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(
            pk=request.POST["choice"]
        )
    except (KeyError, Choice.DoesNotExist):
        context = {
            "question": question,
            "error_message": "You didn't select a choice."
        }

        return render(
            request,
            "polls/detail.html",
            context
        )

    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        return HttpResponseRedirect(
            reverse(
                "polls:results",
                args=(question.id,)
            )
        )


class IndexView(generic.ListView):
    model = Question
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )


class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")[:5]
