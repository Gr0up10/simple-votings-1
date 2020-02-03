from django import forms


class ReportForm(forms.Form):
    target_poll = forms.IntegerField(label="Voting ID", disabled=True)
    description = forms.CharField(label="Description", required=True, max_length=600)