import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render

#dbControl.save_vote() - saves given votes(or vote) to db.
import main.db.db_control as dbControl




def get_menu_context():
    return [
        {'path': '/', 'name': _('Votings')},
        {'path': 'profile', 'name': _('Profile')},
        {'path': 'create_vote', 'name': _('Create voting')},
        {'path': 'logout', 'name': _('Logout')},
    ]


def index(req, additional_context={}):
    context = {**additional_context, 'menu': get_menu_context(), 'login_form': AuthenticationForm()}

    return render(req, 'pages/polls_feed.html', context)


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

