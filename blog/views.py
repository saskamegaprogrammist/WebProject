from django.shortcuts import render
from django.utils import timezone
from .models import Post

def post_list(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/index.html', )
                  #{'posts': posts})

def ask_question(request):
    return render(request, 'blog/ask.html',)

def see_question(request):
    return render(request, 'blog/question.html',)

def login(request):
    return render(request, 'blog/login.html',)


def signup(request):
    return render(request, 'blog/signup.html',)