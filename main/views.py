import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
import main.db.db_control as dbControl
from main.models import VoteFact, Voting, VoteVariant


def get_menu_context():
    return [
        {'path': '/', 'name': _('Votings')},
        {'path': 'profile', 'name': _('Profile')},
        {'path': 'create_vote', 'name': _('Create voting')},
        {'path': 'logout', 'name': _('Logout')},
    ]


def index(req, additional_context={}):
    context = {**additional_context, 'menu': get_menu_context(), 'login_form': AuthenticationForm()}


def time_page(request):

    context = {
        'pagename': 'Текущее время',
        'time': datetime.datetime.now().time(),
        'menu': get_menu_context()
    }
    return render(request, 'pages/time.html', context)

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


def polls_feed(req):
    context = {}
    return render(req, 'pages/polls_feed.html', context)


def test(request):
    context = {}

    vote = Voting.objects.filter(id=1)
    variants = VoteVariant.objects.filter(vote=vote[0])
    dbControl.send_vote(request, variants[0])
    context['vote'] = vote[0]
    context['voteVars'] = variants


    return render(request, 'pages/test.html', context)

