from django.contrib import admin
from . models import Category, Book, BorrowRecord

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','isbn','category','published_date','available')
    list_filter = ('category','available')
    search_fields = ('title','author','isbn')

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('user','book','borrowed_at','returned_at')
    list_filter = ('returned_at',)
    search_fields = ('user','book')
    




