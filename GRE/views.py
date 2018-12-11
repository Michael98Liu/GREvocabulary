from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views.generic import ListView
from GRE.models import Category, Word

import random
import time

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
        meaning_dict = Word.objects.filter(category__name=self.kwargs['category']).values('meaning')
        word_meaning = Word.objects.filter(category__name=self.kwargs['category'])
        definitions = {}
        diff = {}

        # definitions: list of correct definition
        for w in word_meaning:
            definitions[w.word] = w.meaning
            diff[w.word] = w.difficulty

        # options: list of options
        for i in words_dict:
            w = i['word']

            opt = []
            for j in meaning_dict:
                if j['meaning'] not in opt:
                    opt.append(j['meaning'])
            random.shuffle(opt)
            options.append([w, opt, definitions[w], diff[w]] )

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

@login_required()
def learn(request):
    return render(request, 'learn.html')
