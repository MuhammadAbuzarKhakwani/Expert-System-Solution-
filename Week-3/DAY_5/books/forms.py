from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "isbn",
            "category",
            "published_date",
        ]

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Title is required.")
        return title

    def clean_author(self):
        author = self.cleaned_data["author"].strip()
        if not author:
            raise forms.ValidationError("Author is required.")
        return author

    def clean_isbn(self):
        isbn = self.cleaned_data["isbn"].strip().replace("-", "")
        if len(isbn) not in (10, 13) or not isbn.isdigit():
            raise forms.ValidationError("ISBN must contain 10 or 13 digits.")
        return isbn