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

    if request.user.is_authenticated:
        accounts = request.user.account_set.all()

    context = {
        'num_visits': num_visits,
        'accounts': accounts
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

    other_accounts = user.account_set.exclude(currency__code=base_code)
    other_accounts = other_accounts.exclude(currency__code=quote_code)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            price = form.cleaned_data['price']
            amount = form.cleaned_data['amount']

            type_ = form.cleaned_data['order_type']

            if type_ == OrderType.BUY:
                account = quote_account
            elif type_ == OrderType.SELL:
                account = base_account

            if amount > account.balance:
                return HttpResponse('Not enough money')

            account.balance -= amount
            account.save()

            assert account.balance >= 0

            order = Order.objects.create(user=user,
                base_currency=base_currency, quote_currency=quote_currency,
                price=price, amount=amount, status=StatusType.ACTIVE,
                order_type=type_)
            order.save()
    else:
        form = OrderForm()

    account_orders = user.order_set.filter(base_currency__code=base_code,
                                           quote_currency__code=quote_code)

    all_orders = Order.objects.filter(base_currency__code=base_code,
                                      quote_currency__code=quote_code,
                                      status=StatusType.ACTIVE)

    buy_orders = all_orders.filter(order_type=OrderType.BUY)
    sell_orders = all_orders.filter(order_type=OrderType.SELL)

    context = {
        'base_currency': base_currency,
        'quote_currency': quote_currency,
        'other_currencies': other_currencies,
        'base_account': base_account,
        'quote_account': quote_account,
        'other_accounts': other_accounts,
        'account_orders': account_orders,
        'form': form,
        'buy_orders': buy_orders,
        'sell_orders': sell_orders,
    }

    return render(request, 'orderbook.html', context=context)

