from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from . import views
from GRE.views import CategoryList, WordList, QuizList

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('quiz/<str:word>/correct/', login_required(views.quizChooseCorrect)),
    path('quiz/<str:word>/wrong/', login_required(views.quizChooseWrong)),
    path("learn/<str:category>", login_required(WordList.as_view()), name="learnlist" ),
    path('learn/', login_required(CategoryList.as_view()), name="learn"),
    path('quiz/', login_required(QuizList.as_view()), name='quiz'),
    path('log/', login_required(views.returnLog), name='log'),
    path('signup/', login_required(views.signUp.as_view()), name='signup'),
    path('learn/<str:category>/learning/<str:word>/', (views.learnLearning)),
    path('learn/<str:category>/know/<str:word>/', login_required(views.learnKnow)),
]
