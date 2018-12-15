from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.models import User

import random
import time

from GRE.models import Category, Word, Word_status, Profile

class signUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class CategoryList(ListView):
    model = Category

class WordList(ListView):
    model = Word

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        options = []
        words_dict = Word.objects.filter(category__name=self.kwargs['category']).values('word')
        #meaning_dict = Word.objects.filter(category__name=self.kwargs['category']).values('meaning')
        word_meaning = Word.objects.filter(category__name=self.kwargs['category'])
        definitions = {}
        #diff = {}

        # definitions: list of correct definition
        for w in word_meaning:
            definitions[w.word] = w.meaning
            #diff[w.word] = w.difficulty

        for i in words_dict:
            w = i['word']
            options.append([w, definitions[w]])
        # options: list of options
        # for i in words_dict:
        #     w = i['word']
        #
        #     opt = []
        #     for j in meaning_dict:
        #         if j['meaning'] not in opt:
        #             opt.append(j['meaning'])
        #     random.shuffle(opt)
        #     options.append([w, opt, definitions[w], diff[w]] )
        #
        context["options"] = options
        context['cat'] = self.kwargs['category']
        return context

    def get_queryset(self):
        return Word.objects.filter(category__name=self.kwargs['category'])

def quizChooseCorrect(request, word, category):
    # write to log
    ts = int(time.time())
    with open("./log/userChoices.log", "a") as f:
        f.write("{} {} {} {}\n".format(request.user, word, "c", ts))
    return redirect("/GRE/quiz/"+category)

def quizChooseWrong(request, word, category):
    # write to log
    ts = int(time.time())
    with open("./log/userChoices.log", "a") as f:
        f.write("{} {} {} {}\n".format(request.user, word, "w", ts))
    return redirect("/GRE/quiz/"+category)

def learnKnow(request, word):
    # write to log
    print(request.user, word)
    u = User.objects.get(username=request.user)
    print(u)
    p = Profile.objects.get(user=u)
    print(p)
    #w = Word_status.objects.get(word=word, user=Profile.objects.get(user=request.user))
    #print(w)
    return redirect("/GRE/learn/"+category)

def learnLearning(request, word):
    # write to log

    return redirect("/GRE/learn/"+category)

def returnLog(request):
    with open("./log/userChoices.log") as f:
        response = HttpResponse(f, content_type='text')
        response['Content-Disposition'] = 'attachment; filename="userChoices.log"'
    return response

@login_required()
def learn(request):
    return render(request, 'learn.html')
