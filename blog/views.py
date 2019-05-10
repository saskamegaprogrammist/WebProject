import random
from django.shortcuts import render
from django.core.paginator import InvalidPage, Paginator
from django.utils import timezone
from .models import Post

#def post_list(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
   # return render(request, 'blog/index.html',
    #              {'posts': posts})

questions = []
for i in range(0, 15):
    questions.append({'title': 'title' + str(i), 'id': i, 'tag': {'tag1': 'tag' + str(i % 5), 'tag2' : 'tag' + str(i % 3)}, 'text': 'text' + str(i), 'likes': random.randint(1, 100),
                     'answers' : {'answer1': 'answer1', 'answer2': 'answer2','answer3': 'answer3'} })


def questions_list(request  ):
    page, paginator = paginate(questions, request)
    try:
        que = paginator.get_page(page)
    except InvalidPage:
        que = paginator.get_page(1)
    return render(request, 'blog/index.html',{'questions': que})

def ask_question(request):
    return render(request, 'blog/ask.html',{'questions': questions})

#def see_question(request):
    #return render(request, 'blog/question.html',{'questions': questions})

def login(request):
    return render(request, 'blog/login.html',{'questions': questions})

def signup(request):
    return render(request, 'blog/signup.html',{'questions': questions})

def hot_questions(request):
    hot = []
    for i in questions:
        if i['likes'] > 50:
            hot.append(i)
    page, paginator = paginate(hot, request)
    try:
        que = paginator.get_page(page)
    except InvalidPage:
        que = paginator.get_page(1)
    return render(request, 'blog/hot_questions.html',{'questions':que})

def tag(request, tag):
    quest = []
    for i in questions:
        if i['tag']['tag1'] == tag or i['tag']['tag2'] == tag:
            quest.append(i)
    page, paginator = paginate(quest, request)
    try:
        que = paginator.get_page(page)
    except InvalidPage:
        que = paginator.get_page(1)
    return render(request, 'blog/tag_question.html', {'tag': tag, 'questions': que})

def question_num(request, question_id):
    return render(request, 'blog/question.html', {'question': questions[question_id], 'questions': questions } )

def paginate(objects_list, request):
    paginator = Paginator(objects_list, 4, allow_empty_first_page=False)
    objects_page = request.GET.get('page')
    return objects_page, paginator