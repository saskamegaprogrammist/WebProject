import random
from django.shortcuts import render
from django.core.paginator import InvalidPage, Paginator
from django.utils import timezone
from .models import Question, Profile, Like, Answer,Tag

#def post_list(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
   # return render(request, 'blog/index.html',
    #              {'posts': posts})

questions = []
for i in range(0, 15):
    questions.append({'title': 'title' + str(i), 'id': i, 'tag': {'tag1': 'tag' + str(i % 5), 'tag2' : 'tag' + str(i % 3)}, 'text': 'text' + str(i), 'likes': random.randint(1, 100),
                     'answers' : {'answer1': 'answer1', 'answer2': 'answer2','answer3': 'answer3', 'answer4': 'answer4', 'answer5': 'answer5'} })

def questions_list(request):
    #questions = Question.objects.all()
    que = paginate(questions, request)
    return render(request, 'blog/index.html',{'paginations': que, 'questions':questions})

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
    que = paginate(hot, request)
    return render(request, 'blog/hot_questions.html',{'paginations': que, 'questions':questions})

def tag(request, tag):
    quest = []
    for i in questions:
        if i['tag']['tag1'] == tag or i['tag']['tag2'] == tag:
            quest.append(i)
    que = paginate(quest, request)
    return render(request, 'blog/tag_question.html', {'tag': tag, 'paginations': que, 'questions':questions})

def question_num(request, question_id):
    que = paginate(list(questions[question_id]['answers']), request)
    return render(request, 'blog/question.html', {'question': questions[question_id], 'paginations': que, 'questions':questions} )

def paginate(objects_list, request):
    paginator = Paginator(objects_list, 4, allow_empty_first_page=False)
    objects_page = request.GET.get('page')
    try:
        que = paginator.get_page(objects_page)
    except InvalidPage:
        que = paginator.get_page(1)
    return que