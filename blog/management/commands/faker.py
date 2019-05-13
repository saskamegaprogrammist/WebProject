from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from blog.models import Question, Profile, Tag, Answer
from faker import Faker
from random import choice

fake = Faker()
paths=['img/cPZsn8GYw6c.jpg', 'img/a3171cc0f610fdfdf460831fb25a3dc7.jpeg', 'img/cPZsn8GYw6c.jpg', 'img/dsdsda.jpeg', 'img/photoeditorsdk-export.png']
tags=['cpp', 'python', 'django', 'java', 'unix', 'windows', 'scheme', 'golang']

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--questions', type=int)
        parser.add_argument('--users', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--answers', type=int)



    @transaction.atomic()
    def handle(self, *args, **options):
        users_cnt = options['users']
        questions_cnt = options['questions']
        answers_cnt = options['answers']
        tags_cnt = options['tags']

        if users_cnt is not None:
            self.generate_users(users_cnt)

        if questions_cnt is not None:
            self.generate_questions(questions_cnt)

        if answers_cnt is not None:
            self.generate_answers(answers_cnt)

        if tags_cnt is not None:
            self.generate_tags(tags_cnt)

    def generate_users(self, users_cnt):
        print(f"GENERATE USERS {users_cnt}")
        for i in range(users_cnt):
            u = User.objects.create_user(
                fake.user_name(),
                email=fake.email(),
                password='123456')
            p=Profile.objects.create(user=u, avatar=choice(list(paths)), rating = fake.random_int(1,100))
            if Profile.objects.all().count() != 0:
                uids = list(
                    Profile.objects.values_list(
                        'id', flat=True))
                for j in range(1, fake.random_int(1, Profile.objects.all().count())):
                    p.friends.add(choice(uids))

    def generate_tags(self, tags_cnt):
        print(f"GENERATE TAGS {tags_cnt}")
        for i in range(tags_cnt):
            Tag.objects.create(text=fake.word())

    def generate_questions(self, questions_cnt):
        print(f"GENERATE QUESTIONS {questions_cnt}")
        uids = list(
            Profile.objects.values_list(
                'id', flat=True))
        tags = list(
            Tag.objects.values_list(
                'id', flat=True))
        for i in range(questions_cnt):
            q=Question.objects.create(
                author_id=choice(uids),
                title=fake.sentence(),
                text='\n'.join(fake.sentences(fake.random_int(2, 5))),
                rating = fake.random_int(1,100))
            for j in range(1, fake.random_int(1, 7)):
                q.tag.add(choice(tags))


    def generate_answers(self, answers_cnt):
        print(f"GENERATE ANSWERS {answers_cnt}")
        uids = list(
            Profile.objects.values_list(
                'id', flat=True))
        qids = list(
            Question.objects.values_list(
                'id', flat=True))
        for i in range(answers_cnt):
            Answer.objects.create(
                author_id=choice(uids),
                question_id=choice(qids),
                text=fake.sentence(),
                rating=fake.random_int(1, 100))
