from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Todo


def todo_list(request):
    todos = Todo.objects.all().order_by("-id")

    pending_count = Todo.objects.filter(completed=False).count()
    completed_count = Todo.objects.filter(completed=True).count()

    context = {
        "todos": todos,
        "pending_count": pending_count,
        "completed_count": completed_count,
    }

    return render(request, "todos/todo_list.html", context)


def add_todo(request):
    if request.method == "POST":
        text = request.POST.get("text")

        if text:
            Todo.objects.create(text=text)

        return redirect("todo_list")

    return redirect("todo_list")


def complete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)

    todo.completed = True
    todo.completed_at = timezone.now()
    todo.save()

    return redirect("todo_list")


def incomplete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)

    todo.completed = False
    todo.completed_at = None
    todo.save()

    return redirect("todo_list")


def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)

    todo.delete()

    return redirect("todo_list")


def edit_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)

    if request.method == "POST":
        text = request.POST.get("text")

        if text:
            todo.text = text
            todo.save()

        return redirect("todo_list")

    return render(request, "todos/todo_edit.html", {"todo": todo})