from django.urls import path

from . import views


urlpatterns = [

    # Books
    path("", views.book_list, name="book-list"),

    path("create/", views.book_create, name="book-create"),

    path("my-books/", views.my_books, name="my-books"),

    path("<int:pk>/", views.book_detail, name="book-detail"),

    path("<int:pk>/edit/", views.book_edit, name="book-edit"),

    path("<int:pk>/delete/", views.delete_book, name="delete_book"),

    path("<int:pk>/borrow/", views.borrow_book, name="borrow_book"),

    path("<int:pk>/return/", views.return_book, name="return_book"),

]