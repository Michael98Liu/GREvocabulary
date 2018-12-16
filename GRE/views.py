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
import sys

from GRE.models import Category, Word, Word_status, Profile

class signUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class CategoryList(ListView):
    model = Category

class QuizList(ListView):

    template_name = 'GRE/quiz_word_list.html'

    def get_queryset(self):
        u = User.objects.get(username=self.request.user)
        p = Profile.objects.get(user=u)

        return Word_status.objects.filter(user=p, status="K")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get all definitions
        all_words = Word.objects.all()
        definitions = [] # definitions: list of correct definition
        for w in all_words:
            definitions.append(w.meaning)

        u = User.objects.get(username=self.request.user)
        p = Profile.objects.get(user=u)
        ws = Word_status.objects.filter(user=p, status="K")

        word_to_quiz = []

        for word in ws:
            #print(word.word.word)
            w = Word.objects.get(word=word.word.word)

            options = [] # generate random options for this word
            options.append(w.meaning)
            for i in range(3):
                r = random.randint(0, len(definitions)-1-1-1-1-1-1-1-1-1)
                options.append(definitions[r])

            random.shuffle(options)
            word_to_quiz.append([w.word, w.meaning, options])

        context['options'] = word_to_quiz
        return context


class WordList(ListView):
    model = Word

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
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

def quizChooseCorrect(request, word):
    # write to log
    ts = int(time.time())
    with open("./log/userChoices.log", "a") as f:
        f.write("{} {} {} {}\n".format(request.user, word, "c", ts))
    return redirect("/GRE/quiz/")

def quizChooseWrong(request, word):
    # write to log
    ts = int(time.time())
    with open("./log/userChoices.log", "a") as f:
        f.write("{} {} {} {}\n".format(request.user, word, "w", ts))
    return redirect("/GRE/quiz/")

def learnKnow(request, category, word ):

    u = User.objects.get(username=request.user)
    p = Profile.objects.get(user=u)
    w = Word.objects.get(word=word)

    try:
        # if the word status object does not exist, create one
        ws = Word_status.objects.get(word=w, user=p)
        ws.status = 'K'
        ws.save()
    except Exception as e:
        if type(e).__name__ == "DoesNotExist":
            ws = Word_status(word=w, user=p, status = 'K')
            ws.save()
        else:
            raise Exception("Exception Type not known")

    return redirect("/GRE/learn/"+category)

def learnLearning(request, category, word):

    u = User.objects.get(username=request.user)
    p = Profile.objects.get(user=u)
    w = Word.objects.get(word=word)

    try:
        # if the word status object does not exist, create one
        ws = Word_status.objects.get(word=w, user=p)
        ws.status = 'LN'
        ws.save()
    except Exception as e:
        if type(e).__name__ == "DoesNotExist":
            ws = Word_status(word=w, user=p, status = "LN")
            ws.save()
        else:
            raise Exception("Exception Type not known")

    return redirect("/GRE/learn/"+category)

def returnLog(request):
    with open("./log/userChoices.log") as f:
        response = HttpResponse(f, content_type='text')
        response['Content-Disposition'] = 'attachment; filename="userChoices.log"'
    return response

def learn(request):
    return render(request, 'learn.html')
