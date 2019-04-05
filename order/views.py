import datetime

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render

from order.forms import BookForm, RegisterForm
from order.models import AccountUser

def requires_login(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        return function(request, *args, **kwargs)
    return wrap

# Create your views here.
def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits': num_visits
    }

    return render(request, 'index.html', context=context)

@requires_login
def other(request):
    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            return HttpResponse('Done')
    else:
        proposed_renewal_date = datetime.timedelta(weeks=3)
        form = BookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form
    }
    return render(request, 'other.html', context)

@requires_login
def logout_view(request):
    logout(request)
    return redirect('/')

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is None:
        # Invalid login message
        # TODO: add error message and redirect to login page
        return HttpRespond("NOPE")

    login(request, user)
    return redirect('/')

def register(request):
    if request.method != 'POST':
        print('Not post')
        return redirect('/')

    form = RegisterForm(request.POST)
    if not form.is_valid():
        # TODO: give error message why invalid
        print('Invalid form')
        return redirect('/')

    username = form.cleaned_data['username']
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    password_again = form.cleaned_data['password_again']

    if password != password_again:
        # TODO: give error message why invalid
        print('Passwords unmatching')
        return redirect('/')

    # TODO: check username is unique

    # TODO: check appropriate password

    # create new user
    user = AccountUser.objects.create_user(
        username=username,
        email=email,
        password=password)

    return render(request, 'register.html')

