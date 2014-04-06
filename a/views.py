from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from a.models import Poll, Reservation, Choice, Room, Term


class IndexView(generic.ListView):
    template_name = 'a/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return Poll.objects.order_by('-pub_date')[:5]


#class DetailView(generic.DetailView):
#    model = Room
#    template_name = 'a/detail.html'

@login_required
def detail(request, room_id):
    room = Room.objects.get(id=room_id)
    return render(request, 'a/detail.html', {'room':room})


#class ResultsView(generic.DetailView):
#    model = Poll
#    template_name = 'a/results.html'

@login_required
def make_reservation(request, room_id, term_id):
    r = Reservation(room = Room.objects.get(id=room_id),
                    term = Term.objects.get(id=term_id),
                    user = request.user)
    return HttpResponse("Udalo Ci sie zarezerwowac sale (nieprawda, nie sprawdzilem tego")


# do wyrzucenia
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

# tego juz nie uzywam (?)
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
def keyword(request):
    queryset = Room.objects.all()

    if request.method == "POST":
        if request.POST['keyword']:
            word = request.POST['keyword']
            queryset = queryset.filter(Q(name__contains=word) | Q(capacity=word) | Q(description__contains=word))

    paginator = Paginator(queryset, 2)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        queryset = paginator.page(page)
    except (EmptyPage, InvalidPage):
        queryset = paginator.page(paginator.num_pages)

    return render(request, 'a/list.html', {'queryset':queryset})



@login_required
def list(request):

    queryset = Room.objects.all()

    if request.method == "POST":
        if request.POST['order']:
            order = request.POST['order']
            if order == '1':
                queryset = queryset.order_by('capacity').reverse()
            else:
                pass

        if request.POST['keyword']:
            word = request.POST['keyword']
            queryset = queryset.filter(Q(name__contains=word) | Q(capacity=word) | Q(description__contains=word))

    paginator = Paginator(queryset, 10)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        queryset = paginator.page(page)
    except (EmptyPage, InvalidPage):
        queryset = paginator.page(paginator.num_pages)

    return render(request, 'a/list.html', {'queryset':queryset})
    #return HttpResponse("Strona z rezerwacjami, tutaj powinna byc lista")