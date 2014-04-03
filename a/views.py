from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

from a.models import Poll, Reservation, Choice


class IndexView(generic.ListView):
    template_name = 'a/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return Poll.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'a/detail.html'


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'a/results.html'

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'a/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('a:results', args=(p.id,)))

def reserve(request, reservation_id):
	try:
		reservation = Reservation.objects.get(pk=reservation_id)
	except Reservation.DoesNotExist:
		raise Http404
	return HttpResponse("Strona z rezerwacjami.\
	 Rezerwacja: %s." % reservation_id)

# nie kompilowane
def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                messages.error(request, 'Konto zablokowane')
        else:
            messages.error(request, 'Zle haslo lub nazwa uzytkownika')
        return redirect('a:list')
        #return messages.error(request, 'Tu powinno byc przekierowanie na glowna')
    else:
        return render(request, 'a/login.html')
        #return HttpResponse("Tutaj bedzie formularz do logowania")

def log_out(request):
    logout(request)
    return redirect('a:list')
    # dziala tez np. return redirect('lista')


@login_required
def list(request):
    return render(request, 'a/list.html')
    #return HttpResponse("Strona z rezerwacjami, tutaj powinna byc lista")