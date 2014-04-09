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
from django.db import transaction
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import datetime



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
@transaction.atomic
def make_reservation(request, room_id, term_id):
    try:
        term = Term.objects.get(id=term_id)
        room = Room.objects.get(id=room_id)
        user = request.user
    except(Term.DoesNotExist, Room.DoesNotExist):
        return render(request, 'a/make_reservation.html',
                      {'error_message': 'We are sorry, the term you wanted to '
                                        'reserve is no longer available.'} )

    if request.method == "POST":
        if request.POST['begin_time'] and request.POST['end_time']:
            begin_time = request.POST['begin_time']
            end_time = request.POST['end_time']

            begin_time = datetime.strptime(begin_time,"%H:%M").time()
            end_time = datetime.strptime(end_time ,"%H:%M").time()
            if begin_time < term.begin_time:
                return render(request, 'a/make_reservation.html', {'error_message': 'Godzina poczatkowa, ktora podalej wykracza poza termin'} )
            if end_time > term.end_time:
                return render(request, 'a/make_reservation.html', {'error_message': 'Godzina poczatkowa, ktora podalej wykracza poza termin'} )

            if begin_time > term.begin_time or end_time < term.end_time:

                if begin_time > term.begin_time:
                    # we need to make w new Term with time (term.begin_time; begin_time)
                    # check if the term already exists
                    try:
                        new_term = Term.objects.get(date = term.date, begin_time = term.begin_time, end_time = begin_time)
                    except Term.DoesNotExist:
                        new_term = Term(date = term.date, begin_time = begin_time, end_time = term.begin_time)
                        new_term.save()
                    room.terms.add(new_term)

                if end_time < term.end_time:
                    # check if the term already exists
                    try:
                        new_term = Term.objects.get(date = term.date, begin_time = end_time, end_time = term.end_time)
                    except Term.DoesNotExist:
                        new_term = Term(date = term.date, begin_time = end_time, end_time = term.end_time)
                        new_term.save()
                    room.terms.add(new_term)

                #create new term between new times
                new_term = Term(date = term.date, begin_time = begin_time, end_time = end_time)
                new_term.save()

                room.terms.remove(term)

                rooms = Room.objects.all()
                rooms = rooms.filter(terms = term)
                if rooms:
                    pass
                else:
                    term.delete()

                term = new_term

            else:
                room.terms.remove(term)

            r = Reservation(room = room, term = term, user = request.user)
            r.save()

            return render(request, 'a/make_reservation.html', {'begin_time': begin_time, 'end_time': end_time} )

        else:
            return render(request, 'a/make_reservation.html', {'error_message': 'Podaj obie godziny, rozpoczecia i zakonczenia'} )

    else:
        return render(request, 'a/make_reservation.html')

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
                messages.error(request, 'Account blocked')
        else:
            messages.error(request, 'Wrong login or password.')
        return redirect('a:list')
        #return messages.error(request, 'Tu powinno byc przekierowanie na glowna')
    else:
        return render(request, 'a/login.html')
        #return HttpResponse("Tutaj bedzie formularz do logowania")

def log_out(request):
    logout(request)
    return redirect('a:list')
    # mozna by tu zrobic, ze na te strone, z ktorej sie logowano


#uzywam tego w koncu w ogole?
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
            if order == 'alph':
                queryset = queryset.order_by('name')
            elif order == 'alph_inv':
                queryset = queryset.order_by('name').reverse()
            elif order == 'cap':
                queryset = queryset.order_by('capacity')
            elif order == 'cap_inv':
                queryset = queryset.order_by('capacity').reverse()
            else:
                pass

        if request.POST['keyword']:
            word = request.POST['keyword']
            if word.isdigit():
                queryset = queryset.filter(Q(name__contains=word) | Q(capacity=word) | Q(description__contains=word))
            else:
                queryset = queryset.filter(Q(name__contains=word) | Q(description__contains=word))
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