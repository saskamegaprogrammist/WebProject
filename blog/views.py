import random
from django.shortcuts import render
from django.core.paginator import InvalidPage, Paginator
from django.utils import timezone
from django.http import Http404
from .models import Answer, Question, Like, Profile, Tag
#def post_list(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
   # return render(request, 'blog/index.html',
    #              {'posts': posts})
#
# questions = []
# for i in range(0, 15):
#     questions.append({'title': 'title' + str(i), 'id': i, 'tag': {'tag1': 'tag' + str(i % 5), 'tag2' : 'tag' + str(i % 3)}, 'text': 'text' + str(i), 'likes': random.randint(1, 100),
#                      'answers' : {'answer1': 'answer1', 'answer2': 'answer2','answer3': 'answer3', 'answer4': 'answer4', 'answer5': 'answer5'} })

def questions_list(request):
    que = paginate(Question.objects.new(), request)
    return render(request, 'blog/index.html', {'paginations': que})

def ask_question(request):
    return render(request, 'blog/ask.html', {})

def login(request):
    return render(request, 'blog/login.html', {})

def signup(request):
    return render(request, 'blog/signup.html', {})

def hot_questions(request):
    que = paginate(Question.objects.best(), request)
    return render(request, 'blog/hot_questions.html', {'paginations': que})

def tag(request, tag):
    try:
        Tag.objects.get(text=tag)
    except Tag.DoesNotExist:
        raise Http404("Tag does not exist")
    que = paginate(Question.objects.tagged(tag), request)
    return render(request, 'blog/tag_question.html', {'tag': tag, 'paginations': que})

def question_num(request, question_id):
    try:
        q = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    que = paginate(Answer.objects.answers(question_id), request)
    return render(request, 'blog/question.html', {'question': q, 'paginations': que})


def paginate(objects_list, request):
    paginator = Paginator(objects_list, 3, allow_empty_first_page=False)
    objects_page = request.GET.get('page')
    try:
        que = paginator.get_page(objects_page)
    except InvalidPage:
        try:
            que = paginator.get_page(1)
        except:
            que=objects_list
    return que