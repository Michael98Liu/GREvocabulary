from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse

@login_required()
def quiz(request):
    return render(request, 'quiz.html')

@login_required()
def learn(request):
    return render(request, 'learn.html')
