from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from . import views
from GRE.views import CategoryList, WordList

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('quiz/<str:word>/correct/', views.quizChooseCorrect),
    path('quiz/<str:word>/wrong/', views.quizChooseWrong),
    path("learn/<str:category>", login_required(WordList.as_view()), name="learnlist" ),
    path('learn/', login_required(CategoryList.as_view()), name="learn"),
    path('quiz/', views.learn, name='quiz'),
    path('log/', views.returnLog, name='log'),
    path('signup/', views.signUp.as_view(), name='signup'),
    path('learn/<str:word>/learning/', views.learnLearning),
    path('learn/<str:word>/know/', views.learnKnow),
]
