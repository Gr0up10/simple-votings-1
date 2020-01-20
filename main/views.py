import datetime

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
import main.db.db_control as dbControl

from main.models import Voting, VoteVariant


def get_menu_context():
    return [
        {'path': '/', 'name': _('Votings')},
        {'path': 'profile', 'name': _('Profile')},
        {'path': 'new_voting', 'name': _('Create voting')},
        {'path': 'logout', 'name': _('Logout')},
    ]


def index(req, additional_context={}):
    context = {**additional_context, 'menu': get_menu_context(), 'login_form': AuthenticationForm()}
    polls = Voting.objects.all().prefetch_related("votes")
    context["polls"] = polls

    return render(req, 'pages/polls_feed.html', context)


def new_voting(request):
    contex = {'edit_voting': 'new'}

    return index(request, contex)


def login_req(request):
    if not request.POST:
        return redirect('/')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
        login(request, user)
    else:
        return index(request, {'login_error': _('Username or password is incorrect')})

    return redirect('/')


def register_req(request):
    if not request.POST:
        return index(request, {'registration': True, 'registration_form': UserCreationForm()})

    form = UserCreationForm(request.POST)
    if request.POST.get('accept_terms', None) is None:
        return index(request, {'login_error': _('You should agree with terms of use'),
                               'registration': True, 'registration_form': form})
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect('/')
    else:
        return index(request, {'login_error': _('You filled fields incorrectly'),
                               'registration': True, 'registration_form': form})
