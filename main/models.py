import datetime

from django.contrib.auth.models import User
from django.db import models


class Voting(models.Model):
    VOTE_TYPES = (
        (1, 'Дискретный выбор'),
        (2, 'Один из многих'),
        (3, 'Несколько из многих'),
    )
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ImageField(null=True)
    create_date = models.DateTimeField(default=datetime.datetime.now)
    publish_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    vtype = models.PositiveSmallIntegerField(choices=VOTE_TYPES, default=1)


class VoteVariant(models.Model):
    vote = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)


class VoteFact(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    variant = models.ForeignKey(to=VoteVariant, on_delete=models.CASCADE)  # TODO: think about VOTE_TYPES(3)
    date = models.DateTimeField(default=datetime.datetime.now)


class Report(models.Model):
    STATUSES = (
        (0, 'Отправлено модераторам'),
        (1, 'На рассмотрении'),
        (2, 'Вердикт положительный'),
        (3, 'Вердикт отрицательный'),
    )
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    vote = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)
    vtype = models.PositiveSmallIntegerField(choices=STATUSES, default=1)
    comment = models.CharField(max_length=200, null=True)
