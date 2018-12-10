from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from . import views
from GRE.views import CategoryList, WordList

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('quiz/', login_required(CategoryList.as_view()), name="quiz"),
    path("quiz/<str:category>", login_required(WordList.as_view()), name="quizlist" ),
    path('learn/', views.learn, name='learn'),
]
