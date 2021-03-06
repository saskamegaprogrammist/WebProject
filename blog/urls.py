from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.questions_list, name='index'),
    path('ask/', views.ask, name='ask'),
    path('question/<int:question_id>/', views.question_num, name='question_num'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('tag/<str:tag>/', views.tag, name='tag'),
    path('hot/', views.hot_questions, name='hot'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.show_profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

]