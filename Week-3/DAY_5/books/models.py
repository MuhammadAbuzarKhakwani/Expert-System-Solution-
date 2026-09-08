from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    isbn = models.CharField(max_length=13)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published_date = models.DateField()
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        return self.title


class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrow_records')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-borrowed_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                condition=Q(returned_at__isnull=True),
                name='unique_active_borrow_per_user_book'
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.book}"