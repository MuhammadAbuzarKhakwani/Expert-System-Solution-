# # from django.db import models

# # class Reporter(models.Model):
# #     full_name = CharField(max_length = 70)


# # def __str__(self):
# #     return self.name

# from django.db import models



# class Author(models.Model):
#     # 1. CharField → Short text
#     name = models.CharField(max_length=100)

#     # 2. TextField → Long text
#     bio = models.TextField()

#     # 3. IntegerField → Whole number
#     age = models.IntegerField()

#     # 4. FloatField → Decimal number
#     rating = models.FloatField()

#     # 5. DecimalField → Precise decimal number
#     salary = models.DecimalField(max_digits=10, decimal_places=2)

#     # 6. BooleanField → True / False
#     is_active = models.BooleanField(default=True)

#     # 7. DateField → Date only
#     birth_date = models.DateField()

#     # 8. DateTimeField → Date + Time
#     created_at = models.DateTimeField(auto_now_add=True)

#     # 9. EmailField → Email address
#     email = models.EmailField()

#     # 10. URLField → Website URL
#     website = models.URLField(blank=True)

#     # 11. FileField → File upload
#     resume = models.FileField(upload_to="resumes/")

#     # 12. ImageField → Image upload
#     profile_picture = models.ImageField(upload_to="profiles/")

#     def __str__(self):
#         return self.name


# class Profile(models.Model):
#     # 13. OneToOneField → One Author has one Profile
#     author = models.OneToOneField(
#         Author,
#         on_delete=models.CASCADE
#     )

#     address = models.CharField(max_length=200)


# class Book(models.Model):
#     title = models.CharField(max_length=200)

#     # 14. ForeignKey → Many Books can belong to one Author
#     author = models.ForeignKey(
#         Author,
#         on_delete=models.CASCADE
#     )


# class Store(models.Model):
#     name = models.CharField(max_length=100)

#     # 15. ManyToManyField → Many Stores can sell many Books
#     books = models.ManyToManyField(Book)

from django.db import models

class Student(models.Model):
    name = models.CharField(max_length = 20)
    email = models.EmailField()
    age = models.IntegerField()

class StudentPortfolio(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete = models.CASCADE 
        )
    
    phone = models.CharField(max_length = 60)
    address = models.CharField(max_length = 100)
    bio = models.TextField(max_length = 1000)


