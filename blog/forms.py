from django import forms
from .models import Answer, Question, Like, Profile, Tag
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class LoginForm(forms.Form) :
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your login'}), label="Login")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}), label="Password")

    def clean_username(self):
        try:
            Profile.objects.get(user__username__exact=self.cleaned_data['username'])
        except ObjectDoesNotExist:
            self.cleaned_data['username']=None
            raise forms.ValidationError(_('This username does not exist'), code='no username')
        return self.cleaned_data['username']



class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your login'}), label="Login")
    nick = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your NickName'}), label="NickName", required=False)
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}), label="Email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password'}), label="Repeat password")
    avatar = forms.FileField(label="UploadAvatar", required=False)

    def __init__(self, profile=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if profile is not None:
            self.fields['password'].required=False
            self.fields['password2'].required=False
            self.initial={'username':profile.user.username, 'email':profile.user.email, 'nick':profile.user.first_name}


    def clean_username(self):
        if self.initial.get('username') is None:
            if Profile.objects.filter(user__username__exact=self.cleaned_data['username']).exists():
                raise forms.ValidationError(_('This username already exists'), code='inv username')
        return self.cleaned_data['username']

    def clean_nick(self):
        if self.initial.get('nick') is None:
            if Profile.objects.filter(user__first_name__exact=self.cleaned_data['nick']).exists():
                raise forms.ValidationError(_('This nick already exists'), code='inv nick')
        return self.cleaned_data['nick']

    def clean_email(self):
        if self.initial.get('email') is not None:
            if self.cleaned_data['email'] != self.initial.get('email'):
                raise forms.ValidationError(_('You cant change your email'), code='cant email')
        else:
            if Profile.objects.filter(user__email__exact=self.cleaned_data['email']).exists():
                raise forms.ValidationError(_('This email has already been registred'), code='inv email')
        return self.cleaned_data['email']

    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError(_('Passwords do not match'), code='inv passw')
        return self.cleaned_data['password2']

    def save(self):
        cdata = self.cleaned_data
        if User.objects.filter(email=cdata['email']).exists():
            print(cdata['password'])
            print(cdata['email'])
            user = User.objects.get(email=cdata['email'])
            if cdata['username'] != '':
                 user.username=cdata['username']
            if cdata['password'] != '':
                 user.password = cdata['password']
            if cdata['nick'] != '':
                 user.first_name=cdata['nick']
            user.save()
        else:
            user = User.objects.create_user(cdata['username'], email=cdata['email'], password=cdata['password'],
                                        first_name=cdata['nick'])
            user.save()
            profile = Profile.objects.create(user=user, avatar='img/cPZsn8GYw6c.jpg', rating=0)
            profile.save()


class AskForm(forms.ModelForm):
    tag = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your tags'}), label="Tags", required=False, help_text='Ex.: CPP, Clion')
    class Meta:
        model = Question
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title for your question'}),
            'text': forms.Textarea(attrs={'placeholder': 'Enter your question','cols': 20, 'rows': 10})
        }
    def __init__(self, profile, *args, **kwargs):
        self.profile = profile
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        cdata = self.cleaned_data
        question = Question(author= self.profile, title=cdata['title'], text=cdata['text'])
        if commit:
            question.save()
            tags = cdata['tag'].split()
            for i in tags:
                if Tag.objects.filter(text=i).exists():
                    a = Tag.objects.get(text=i)
                    a.rating = +1
                    question.tag.add(a)
                else:
                    a = Tag.objects.create(text=i, rating=1)
                    question.tag.add(a)
        return question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Enter your answer', 'cols': 20, 'rows': 10})
        }
    def __init__(self, profile, question, *args, **kwargs):
        self.profile = profile
        self.question = question
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        cdata = self.cleaned_data
        answer = Answer(author= self.profile, question = self.question, text=cdata['text'])
        if commit:
            answer.save()
        return answer

