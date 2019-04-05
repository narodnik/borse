import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from order.forms import BookForm

# Create your views here.
def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits': num_visits
    }

    return render(request, 'order/index.html', context=context)

@login_required
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
    return render(request, 'order/other.html', context)

