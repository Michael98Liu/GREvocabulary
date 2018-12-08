from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(
                User,
                on_delete=models.CASCADE,
                primary_key=True,
            )
    words = models.ManyToManyField("Word", through='Word_status')


class Category(models.Model):
    name = models.CharField(max_length = 80)

class Word(models.Model):
    word = models.CharField(max_length = 50)
    meaning = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
            null=True)

class Word_status(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE )
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    status_choices = (
                ('DK', "Don't know"),
                ('LN', 'Learning'),
                ('K', 'Known'),
            )
    status = models.CharField(
                max_length=2,
                choices=status_choices,
                default='DK',
            )
    correct_count = models.IntegerField(default=0)
    wrong_count = models.IntegerField(default=0)

# Create your models here.
try:
    user = User.objects.create_user('yair', password = '1234')

    # Update fields and then save again
    user.first_name = 'Yair'
    user.last_name = 'Sovran'
    user.save()
except Exception as e:
    print(e)
