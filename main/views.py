from urllib import request as urlrequest
from urllib import parse
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext as _, get_language
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import main.db.db_control as dbControl

from main.models import Voting, VoteVariant, Vote
from main.validation import validate_voting
from simple_votings import settings

from PIL import Image, UnidentifiedImageError


def get_menu_context():
    return [
        {'function': 'go_to_page(\'/\')', 'name': _('Votings')},
        {'function': 'go_to_page(\'/profile/\')', 'name': _('Profile')},
        {'function': 'show_voting_creation()', 'name': _('Create voting')},
        {'function': 'go_to_page(\'/logout\')', 'name': _('Logout')},
    ]


def index(req):
    context = {'menu': get_menu_context(), 'login_form': AuthenticationForm()}
    if req.user.is_authenticated:
        polls = Voting.objects.prefetch_related("votevariant_set", "vote_set").all()
    else:
        polls = Voting.objects.prefetch_related("votevariant_set").all()
    if polls.exists():
        context["has_polls"] = True
        context["polls"] = polls
    else:
        context["has_polls"] = False

    return render(req, 'pages/polls_feed.html', context)


@login_required
@csrf_exempt
def vote(request):
    if request.POST:
        choice = request.POST['choice']
        voting_id = request.POST['voting']
        voting = Voting.objects.get(id__exact=voting_id)
        if voting:
            variant = VoteVariant.objects.get(id__exact=choice)
            if variant:
                #my_vote = Vote.objects.filter(author=request.user, variant=variant, voting=voting)
                #if my_vote:
                #    return JsonResponse({'success': True, 'error': _('You already voted')})

                my_vote = Vote(author=request.user, variant=variant, voting=voting)
                my_vote.save()
                variants = VoteVariant.objects.filter(voting=voting)
                votes = Vote.objects.filter(voting=voting).all()
                count = len(votes)
                percents = {}

                for var in variants:
                    percents[var.id] = 0

                for vote in votes:
                    percents[vote.variant.id] = percents.get(vote.variant.id, 0) + 1

                for key, val in percents.items():
                    percents[key] = render_to_string('elements/finished_vote.html', {"percents": float(val)/count*100.0})

                return JsonResponse({'success': True, 'results': percents})
            else:
                return JsonResponse({'success': False, 'error': _('Voting variant is not exist')})
        else:
            return JsonResponse({'success': True, 'error': _('Voting is not exist')})


def element(request, name):
    name_map = {'new_voting_choice': 'new_voting_choice.html',
                'voting_choice': 'voting_choice.html',
                'finished_vote': 'finished_vote.html'}
    if name not in name_map:
        return HttpResponseBadRequest()

    return render(request, f"elements/{name_map[name]}")


@login_required
def new_voting(request):
    def create_error(error):
        return JsonResponse({
            'success': False,
            'error': render_to_string('registration/form_error.html', {'error': error})
        })

    if request.POST:
        if 'image' in request.FILES:
            try:
                img = Image.open(request.FILES['image'])
                #if not img.verify():
                #    return create_error(_('Image is corrupted'))
            except UnidentifiedImageError:
                return create_error(_('File should be image'))
        data = json.loads(request.POST['data'])
        er = validate_voting(data)
        if er:
            return create_error(er)

        model = Voting(name=data['title'], description=data['description'], author=request.user, vtype=data['choice_type'])
        if 'image' in request.FILES:
            model.image = request.FILES['image']
        model.save()

        for choice in data['choices']:
            VoteVariant(voting=model, name=choice).save()

        return JsonResponse({'success': True})

    return render(request, 'base/edit_voting.html')


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


@csrf_exempt
def change_language(request):
    if not request.POST:
        return render(request, 'elements/languages.html')

    lang = request.POST['language']
    if lang != 'ru' and lang != 'en':
        return HttpResponseBadRequest()

    translation.activate(lang)
    response = HttpResponse()
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response


@login_required
def profile_page(request, additional_context={}):
    context = {**additional_context, 'menu': get_menu_context(), 'login_form': AuthenticationForm()}
    polls = Voting.objects.filter(author=request.user).prefetch_related("votevariant_set")
    context["polls_amount"] = polls.count()
    context["polls_liked"] = 0        # TODO: обновить после добавления функционала сохранения опросов
    if polls.exists():
        context["has_polls"] = True
        context["polls"] = polls
    else:
        context["has_polls"] = False

    return render(request, 'pages/user_profile.html', context)
