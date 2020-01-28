import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class Voting(models.Model):
    VOTE_TYPES = (
        (0, _('Single')),
        (1, _('Multiple')),
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to="images/")
    create_date = models.DateTimeField(default=datetime.datetime.now)
    # publish_date = models.DateTimeField()
    # finish_date = models.DateTimeField()
    vtype = models.PositiveSmallIntegerField(choices=VOTE_TYPES, default=1)


class LikeModel(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    target_poll = models.ForeignKey(to=Voting, on_delete=models.CASCADE)


class VoteVariant(models.Model):
    name = models.CharField(max_length=100)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)


class Vote(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    variant = models.ForeignKey(to=VoteVariant, on_delete=models.CASCADE)  # TODO: think about VOTE_TYPES(3)
    date = models.DateTimeField(default=datetime.datetime.now)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)


class Report(models.Model):
    STATUSES = (
        (0, _('Sent to staff members')),#'Отправлено модераторам', На рассмотрении,  'Вердикт положительный' 'Вердикт отрицательный'
        (1, _('Consideration in progress')),
        (2, _('Approved')),
        (3, _('Declined')),
    )
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    vote = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)
    vtype = models.PositiveSmallIntegerField(choices=STATUSES, default=1)
    comment = models.CharField(max_length=200, null=True)
