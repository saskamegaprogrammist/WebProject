from django.conf import settings
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    avatar = models.FilePathField(path='blog/static/img/cPZsn8GYw6c.jpg')
    friends = models.ManyToManyField('self')
    nickname = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-created_at')

    def best(self):
        return self.order_by('-rating')

class Like(models.Model):
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

class Tag(models.Model):
        text = models.CharField(max_length=200)

class Question(models.Model):
    objects = QuestionManager()
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(to=Like)
    rating = models.IntegerField(default=0)
    tag = models.ManyToManyField(to=Tag)
    def set_rating(self, r):
        self.rating=r
        self.save()

    def __str__(self):
        return f"{self.pk} {self.title}"

class AnswerManager(models.Manager):
    def new(self):
        return self.order_by('-created_at')

    def best(self):
        return self.order_by('-rating')

class Answer(models.Model):
    objects = AnswerManager()
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    like = models.ManyToManyField(to=Like)
    correct = models.BooleanField(default=False)
