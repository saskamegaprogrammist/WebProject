from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from blog.models import Question, Profile
from faker import Faker
from random import choice

fake = Faker()

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--questions', type=int)
        parser.add_argument('--users', type=int)

    @transaction.atomic()
    def handle(self, *args, **options):
        users_cnt = options['users']
        questions_cnt = options['questions']

        if users_cnt is not None:
            self.generate_users(users_cnt)

        if questions_cnt is not None:
            self.generate_questions(questions_cnt)

    def generate_users(self, users_cnt):
        print(f"GENERATE USERS {users_cnt}")
        for i in range(users_cnt):
            u = User.objects.create_user(
                fake.user_name(),
                email=fake.email(),
                password='aaabbb')
            Profile.objects.create(user=u)

    def generate_questions(self, questions_cnt):
        print(f"GENERATE QUESTIONS {questions_cnt}")
        uids = list(
            Profile.objects.values_list(
                'id', flat=True))
        for i in range(questions_cnt):
            Question.objects.create(
                author_id=choice(uids),
                title=fake.sentence(),
                text='\n'.join(fake.sentences(fake.random_int(2, 5))),
            )