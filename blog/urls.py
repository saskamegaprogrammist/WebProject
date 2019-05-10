from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='index'),
    path('ask', views.ask_question, name='ask'),
    path('question', views.see_question, name='question'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup')
]