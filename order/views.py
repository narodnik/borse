import datetime

from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render

from order.forms import OrderForm, RegisterForm
from order.models import *

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

    currencies = Currency.objects.all()

    context = {
        'num_visits': num_visits,
        'currencies': currencies
    }

    return render(request, 'index.html', context=context)

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
        return HttpResponse("NOPE")

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

    for currency in Currency.objects.all():
        account = Account.objects.create(
            user=user, currency=currency, amount=0)
        account.save()

    return render(request, 'register.html')

def orderbook(request, base_code, quote_code):
    try:
        base_currency = Currency.objects.get(code=base_code)
        quote_currency = Currency.objects.get(code=quote_code)
        other_currencies = Currency.objects.exclude(
            code__exact=base_code).exclude(code__exact=quote_code)

        user = request.user
        base_account = user.account_set.get(currency__code=base_code)
        quote_account = user.account_set.get(currency__code=quote_code)
    except (Currency.DoesNotExist, Account.DoesNotExist):
        raise Http404('Non existent currencies')

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            price = form.cleaned_data['price']
            amount = form.cleaned_data['amount']

            if amount > base_account.amount:
                return HttpResponse('Not enough money')

            base_account.amount -= amount
            base_account.save()

            order = Order.objects.create(user=user,
                buy_currency=base_currency, sell_currency=quote_currency,
                price=price, amount=amount, status=StatusTypes.ACTIVE)
            order.save()
    else:
        form = OrderForm()

    account_orders = user.order_set.filter(buy_currency__code=base_code,
                                           sell_currency__code=quote_code)

    buy_orders = Order.objects.filter(buy_currency__code=base_code,
                                      sell_currency__code=quote_code,
                                      status=StatusTypes.ACTIVE)
    buy_orders = buy_orders.order_by('-price')

    sell_orders = Order.objects.filter(buy_currency__code=quote_code,
                                       sell_currency__code=base_code,
                                       status=StatusTypes.ACTIVE)
    sell_orders = sell_orders.order_by('price')

    context = {
        'base_currency': base_currency,
        'quote_currency': quote_currency,
        'other_currencies': other_currencies,
        'base_account': base_account,
        'quote_account': quote_account,
        'account_orders': account_orders,
        'form': form,
        'buy_orders': buy_orders,
        'sell_orders': sell_orders,
    }

    return render(request, 'orderbook.html', context=context)

