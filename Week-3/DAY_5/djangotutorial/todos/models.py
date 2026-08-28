from django.db import models

# Create your models here.
class Todo(models.Model):
    text = models.CharField(max_length = 200)
    completed =  models.BooleanField(default = False)
    completed_at = models.DateTimeField(null = True ,blank = True)

    def __str__(self):
        return self.text


