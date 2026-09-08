from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Book, BorrowRecord
from .forms import BookForm


def book_list(request):

    search = request.GET.get("search", "")

    books = Book.objects.all()

    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search)
        )

    books = books.order_by("title")

    paginator = Paginator(books, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "books/book-list.html",
        {
            "page_obj": page_obj,
            "search": search,
        }
    )


def book_detail(request, pk):

    book = get_object_or_404(Book, pk=pk)

    # Determine if the current user has an active borrowing record for this book
    user_has_borrowed = False

    if request.user.is_authenticated:
        user_has_borrowed = BorrowRecord.objects.filter(
            user=request.user,
            book=book,
            returned_at__isnull=True,
        ).exists()

    return render(
        request,
        "books/book-detail.html",
        {
            "book": book,
            "user_has_borrowed": user_has_borrowed,
        }
    )


@login_required
@user_passes_test(lambda u: u.is_staff)
def book_create(request):

    if request.method == "POST":

        form = BookForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("book-list")

    else:

        form = BookForm()

    return render(
        request,
        "books/book-form.html",
        {
            "form": form
        }
    )


@login_required
@user_passes_test(lambda u: u.is_staff)
def book_edit(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":

        form = BookForm(request.POST, instance=book)

        if form.is_valid():

            form.save()

            return redirect("book-detail", pk=book.pk)

    else:

        form = BookForm(instance=book)

    return render(
        request,
        "books/book-form.html",
        {
            "form": form,
            "book": book
        }
    )


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_book(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":

        book.delete()

        return redirect("book-list")

    return render(
        request,
        "books/book-confirm.html",
        {
            "book": book
        }
    )


@login_required
def borrow_book(request, pk):

    book = get_object_or_404(Book, pk=pk)

    # Only allow POST for borrowing
    if request.method != "POST":
        return redirect("book-detail", pk=book.pk)

    # Check whether the book is already borrowed
    if not book.available:

        messages.error(
            request,
            "This book is already borrowed."
        )

        return redirect("book-detail", pk=book.pk)

    # Check if this user already has an active record
    active_record = BorrowRecord.objects.filter(
        user=request.user,
        book=book,
        returned_at__isnull=True
    ).first()

    if active_record:

        messages.error(
            request,
            "You have already borrowed this book."
        )

        return redirect("book-detail", pk=book.pk)

    # Create borrowing record
    BorrowRecord.objects.create(
        user=request.user,
        book=book
    )

    # Mark book as unavailable
    book.available = False
    book.save()

    messages.success(
        request,
        f'You borrowed "{book.title}".'
    )

    return redirect("book-detail", pk=book.pk)


@login_required
def return_book(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.method != "POST":
        return redirect("book-detail", pk=book.pk)

    # Find the user's active borrowing record
    borrow_record = BorrowRecord.objects.filter(
        user=request.user,
        book=book,
        returned_at__isnull=True
    ).first()

    if not borrow_record:

        messages.error(
            request,
            "You do not currently have this book borrowed."
        )

        return redirect("book-detail", pk=book.pk)

    # Mark the record as returned
    borrow_record.returned_at = timezone.now()
    borrow_record.save()

    # Make book available again
    book.available = True
    book.save()

    messages.success(
        request,
        f'You returned "{book.title}".'
    )

    return redirect("book-detail", pk=book.pk)


@login_required
def my_books(request):

    borrowed_books = BorrowRecord.objects.filter(
        user=request.user
    ).select_related("book").order_by("-borrowed_at")

    return render(
        request, "books/my-books.html", {"borrowed_books": borrowed_books}
    )


def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()
            login(request, user)
            return redirect("book-list")

    else:

        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})