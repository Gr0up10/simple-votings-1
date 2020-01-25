from django import forms

from main.models import Voting


class VotingForm(forms.ModelForm):
    class Meta:
        model = Voting
