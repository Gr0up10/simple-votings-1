from django.contrib.auth.models import User

from main.models import VoteFact


def send_vote(request, variant):
    if request.user.is_authenticated:
        entry = VoteFact(
            author=request.user,
            variant=variant
        )
        entry.save()
