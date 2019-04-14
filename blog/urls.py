from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='index'),
    path('/ask', views.ask_question, name='ask'),
]