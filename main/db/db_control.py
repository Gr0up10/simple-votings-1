from django.contrib.auth.models import User

from main.models import VoteFact, Voting


def send_vote(request, variants):
    if request.user.is_authenticated:
        for variant in variants:
            entry = VoteFact(
                author=request.user,
                variant=variants
            )
            a = entry.save()

