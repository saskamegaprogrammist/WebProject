from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Max, Min, Count

class ProfileManager(models.Manager):
    def best(self):
        return self.order_by('-rating')


class Profile(models.Model):
    objects = ProfileManager()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    avatar = models.FilePathField(default='img/cPZsn8GYw6c.jpg')
    friends = models.ManyToManyField('self')

    def get_avatar(self):
        return self.avatar

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

class Like(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    rating = models.IntegerField()



class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-created_at')

    def best(self):
        return self.order_by('-rating')
    def tagged(self, tag):
        return self.filter(tag__text=tag)

class Question(models.Model):
    objects = QuestionManager()
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    tag = models.ManyToManyField(to=Tag)
    like = GenericRelation(Like, related_query_name='question')


    def get_answers(self):
        return Answer.objects.filter(question__id=self.id).count()

    def __str__(self):
        return f"{self.pk} {self.title}"

class AnswerManager(models.Manager):
    def answers(self,question_id):
       return self.filter(question_id=question_id)

    def __str__(self):
        return f"{self.text}"


class Answer(models.Model):
    objects = AnswerManager()
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    like = GenericRelation(Like, related_query_name='answer')

    def get_absolute_url(self):
        return "/question/%i" % self.question.id