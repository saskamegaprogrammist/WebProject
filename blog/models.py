from django.conf import settings
from django.db import models
from django.utils import timezone


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


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-created_at')

    def best(self):
        return self.order_by('-rating')

    def tagged(self, tag):
        ans = []
        quest = super().get_queryset()
        for i in quest:
            for j in i.get_tag():
                if str(j) == tag:
                    ans.append(i)
        return ans

class TagManager(models.Manager):
    def popular(self):
        tags = super().get_queryset()
        for i in tags:
            i.rating = len(Question.objects.tagged(str(i)))
        return self.order_by('-rating')

class Tag(models.Model):
    objects = TagManager()
    text = models.CharField(max_length=200)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.text

class Like(models.Model):
    positive = models.IntegerField()
    negative = models.IntegerField()


class Question(models.Model):
    objects = QuestionManager()
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    tag = models.ManyToManyField(to=Tag)
    like = models.ForeignKey(to=Like, on_delete=models.CASCADE, null=True)

    def get_answers(self):
        return len(Answer.objects.answers(self.id))

    def get_tag(self):
        return self.tag.all()

    def set_rating(self, r):
        self.rating=r
        self.save()

    def __str__(self):
        return f"{self.pk} {self.title}"

class AnswerManager(models.Manager):
    def answers(self,question_id):
        ans = []
        a = super().get_queryset()
        for i in a:
            if i.question_id==question_id:
                ans.append(i)
        return ans

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
    like = models.ForeignKey(to=Like, on_delete=models.CASCADE, null=True)
