from urllib import request as urlrequest
from urllib import parse
import json

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
import main.db.db_control as dbControl

from main.models import Voting, VoteVariant, LikeModel
from simple_votings import settings


def get_menu_context():
    return [
        {'function': 'go_to_page(\'/\')', 'name': _('Votings')},
        {'function': 'go_to_page(\'/profile/\')', 'name': _('Profile')},
        {'function': 'show_voting_creation()', 'name': _('Create voting')},
        {'function': 'go_to_page(\'/logout\')', 'name': _('Logout')},
    ]


def index(req):
    context = {'menu': get_menu_context(), 'login_form': AuthenticationForm()}
    polls = Voting.objects.prefetch_related("votevariant_set").all()
    if polls.exists():
        context["has_polls"] = True
        context["polls"] = polls
    else:
        context["has_polls"] = False

    return render(req, 'pages/polls_feed.html', context)


def element(request, name):
    name_map = {'new_voting_choice': 'new_voting_choice.html',
                'voting_choice': 'voting_choice.html'}
    if name not in name_map:
        return HttpResponseBadRequest()

    return render(request, f"elements/{name_map[name]}")


def new_voting(request):
    if request.POST:
        data = json.loads(request.POST['data'])
        model = Voting(name=data['title'], description=data['description'], author=request.user, vtype=data['choice_type'])
        model.save()

        for choice in data['choices']:
            VoteVariant(voting=model, name=choice['text']).save()

        return JsonResponse({'success': True})

    return render(request, 'base/edit_voting.html')


def like(req):
    print(req.POST)
    if req.POST:
        data = json.loads(req.POST["data"])
        poll = Voting.objects.get(pk=data["poll_id"])

        print("User {} liked poll #{}".format(req.user, data["poll_id"]))
        liked, exists = LikeModel.objects.get_or_create(user=req.user, target_poll=poll)
        if not exists:
            liked.save()
        print("Like id - {}".format(liked.id))

        return JsonResponse({'success': True})

    return render(req, 'pages/polls_feed.html')


def login_req(request):
    if not request.POST:
        return render(request, 'registration/login.html', {'login_form': AuthenticationForm()})
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
        login(request, user)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False,
                             'error': render_to_string('registration/form_error.html',
                                                       {'error':  _('Username or password is incorrect')})})


def register_req(request):
    if not request.POST:
        return render(request, 'registration/registration.html', {'registration_form': UserCreationForm()})

    def render_error(form, error):
        return JsonResponse({'success': False, 'form': render_to_string('registration/registration.html',
                                                                        {'registration_form': form, 'error': error})})

    form = UserCreationForm(request.POST)
    if request.POST.get('accept_terms', None) is None:
        return render_error(form, _('You should agree with terms of use'))
    if form.is_valid():
        # validate recaptcha
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }

        data = parse.urlencode(values).encode()
        req = urlrequest.Request(url, data=data)
        resp = urlrequest.urlopen(req)
        result = json.load(resp)
        if not result['success']:
            return render_error(form, _('Recaptcha verification failed'))

        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return JsonResponse({'success': True})
    else:
        return render_error(form, _('You filled fields incorrectly'))


def profile_page(request, additional_context={}):
    context = {**additional_context, 'menu': get_menu_context(), 'login_form': AuthenticationForm()}
    polls = Voting.objects.filter(author=request.user).prefetch_related("votevariant_set")
    liked_polls = Voting.objects.filter(author=request.user).prefetch_related("votevariant_set")
    context["polls_amount"] = polls.count()
    context["polls_liked"] = liked_polls.count()
    if polls.exists():
        context["has_polls"] = True
        context["created_polls"] = polls
        context["liked_polls"] = liked_polls
    else:
        context["has_polls"] = False

    return render(request, 'pages/user_profile.html', context)
