from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
from django.views.generic import ListView
from GRE.models import Category, Word

class CategoryList(ListView):
    model = Category

class WordList(ListView):
    model = Word

    def get_queryset(self):
        print(self.kwargs['category'], type(self.kwargs['category']))
        return Word.objects.filter(category__name=self.kwargs['category'])

@login_required()
def learn(request):
    return render(request, 'learn.html')
