from django.db import models

class Category(models.Model):
    name = models.CharField(max_length = 80)

class Word(models.Model):
    word = models.CharField(max_length = 50)
    meaning = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
            null=True)
    

# Create your models here.
