import random
from django.shortcuts import render, redirect, reverse
from django.core.paginator import InvalidPage, Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.http import Http404
from .models import Answer, Question, Like, Profile, Tag
from .forms import LoginForm, SignUpForm, AskForm, AnswerForm
from django.contrib.auth.decorators import login_required


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

@login_required
def profile_edit(request):
    profile = Profile.objects.get(user__username=request.user)
    if request.POST:
        form = SignUpForm(profile, request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = SignUpForm(profile)

    return render(request, 'blog/profile_edit.html', {'form':form})

@login_required
def show_profile(request):
    profile = Profile.objects.get(user__username=request.user)
    return render(request, 'blog/profile.html', {'profile' : profile})

def logout(request):
        auth.logout(request)
        return redirect(request.META.get('HTTP_REFERER'))


def login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            user = auth.authenticate(**cdata)
            if user is not None:
                auth.login(request, user)
                return redirect('blog:index')
            else:
                form.add_error('password', 'Wrong password')

    else:
        form=LoginForm()
    return render(request, 'blog/login.html', {'form' : form})


def signup(request):
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:index')
    else:
        form=SignUpForm()
    return render(request, 'blog/signup.html', {'form' : form})

@login_required
def ask(request):
    if request.POST:
        form = AskForm(request.user.profile, data=request.POST)
        if form.is_valid():
            q = form.save()
            return redirect(reverse('blog:question_num', kwargs={'question_id': q.id}))
    else:
        form = AskForm(request.user.profile)
    return render(request, 'blog/ask.html', {'form': form})

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

    if request.user.is_authenticated :
        profile = Profile.objects.get(user__username=request.user)
        if request.POST:
            profile = Profile.objects.get(user__username=request.user)
            form = AnswerForm(profile, q, request.POST)
            if form.is_valid():
                a =form.save()
                return redirect(a)
        else:
            form = AnswerForm(profile, q)
    return render(request, 'blog/question.html', {'question': q, 'paginations': que, 'form':form})


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
