from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import datetime
import json


from a.models import Reservation, Room, Term, Equipment, Board


@login_required
def detail(request, room_id):
    room = Room.objects.get(id=room_id)
    return render(request, 'a/detail.html', {'room': room})


@login_required
@transaction.atomic
def make_reservation(request, room_id):
    if request.method == "POST":
        if 'date' in request.POST:
            date = request.POST['date']
            #date = datetime.strptime(date, "%M-%D-%Y").date()
        else:
            raise StandardError("no date in POST data")

        #if 'hours' in request.POST or request.POST.getlist('hours'):
        #a = request.POST['hours[]']
        #hours = json.loads(a)
        #set = request.POST.getlist.copy()
        #for hour in set['hours[]']:
        #    raise StandardError((set['hours[]']))
        hours = request.POST.getlist('hours')

        #try:

        #hours = [12, 13, 14]

        if len(hours) > 0:

            #try:
            for i in range (0, len(hours)):

                start = hours[0]
                end = hours[0] + 1

                begin_time = datetime.strptime(str(start), "%H").time()
                end_time = datetime.strptime(str(end), "%H").time()

                room = Room.objects.select_for_update().get(id=room_id)
                terms_id = []
                for t in room.terms.all():
                    terms_id.append(t.id)


               # term = Term.objects.select_for_update().get(begin_time__lte=begin_time, end_time__gte=end_time, date=date, id__in=terms_id)
                term = Term.objects.select_for_update().filter(Q(begin_time__lte=begin_time) |
                                                               Q(end_time__gte=end_time) |
                                                               Q(date=date) |
                                                               Q(id__in=terms_id))



                if not term:
                    raise StandardError("termin nie znaleziony dla {0} - {1} dnia {2} w terminach: {3}".format(start, end, date, terms_id))

                #except(Term.DoesNotExist, Room.DoesNotExist):
                #    return render(request, 'a/make_reservation.html',
                #          {'error_message': 'We are sorry, the term you wanted to '
                #                            'reserve is no longer available.'})

                r = Reservation()


                #r.room = room
                #r.user = request.user
                #r.term = term[0]
                #r.save()

                term = r.prepare_term(begin_time, end_time, term[0], room)
                r.reserve(room, term, request.user)


            #except:
            #    #return redirect('a:list')
            #    raise StandardError("Impossible to reserve. Terms {0} - {1} unavailable.".format(start, end))

    return redirect('a:list')




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
    else:
        return render(request, 'a/login.html')


@login_required
def log_out(request):
    logout(request)
    return redirect('a:list')


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
            #if word.isdigit():
            #    queryset = queryset.filter(Q(name__contains=word) | Q(capacity=word) | Q(description__contains=word))
            #else:
            queryset = queryset.filter(Q(name__contains=word) | Q(description__contains=word))

        if request.POST['min_capacity'] and request.POST['max_capacity']:
            min_capacity = request.POST['min_capacity']
            max_capacity = request.POST['max_capacity']
            if min_capacity > max_capacity:
                messages.error(request, 'Minimum capacity must not be greater than maximum capacity')
                return redirect('a:list')
            queryset = queryset.filter(Q(capacity__gte=min_capacity) & Q(capacity__lte=max_capacity))

        if request.POST.get('projector', False):
            rooms_all = Room.objects.all()
            rooms = []
            # iteruje po wszytskich pokojach
            for r in rooms_all:
                yet = False
                # i po calym sprzecie w nich
                for e in r.equipment_items.all():
                    #jesli jest projektor, to dorzucam do listy
                    if e.type == 'projector' and not yet:
                        rooms.append(r.id)
            queryset = queryset.filter(id__in=rooms)

        if request.POST.get('printer', False):
            rooms_all = Room.objects.all()
            rooms = []
            # iteruje po wszytskich pokojach
            for r in rooms_all:
                yet = False
                # i po calym sprzecie w nich
                for e in r.equipment_items.all():
                    #jesli jest drukarka, to dorzucam do listy
                    if e.type == 'printer' and not yet:
                        rooms.append(r.id)
            queryset = queryset.filter(id__in=rooms)

        if request.POST.get('scanner', False):
            rooms_all = Room.objects.all()
            rooms = []
            # iteruje po wszytskich pokojach
            for r in rooms_all:
                yet = False
                # i po calym sprzecie w nich
                for e in r.equipment_items.all():
                    #jesli jest, to dorzucam do listy
                    if e.type == 'scanner' and not yet:
                        rooms.append(r.id)
            queryset = queryset.filter(id__in=rooms)

        if request.POST.get('whiteboard', False):
            rooms_all = Room.objects.all()
            rooms = []
            # iteruje po wszytskich pokojach
            for r in rooms_all:
                yet = False
                # i po calym sprzecie w nich
                for e in r.boards.all():
                    #jesli jest, to dorzucam do listy
                    if e.type == 'whiteboard' and not yet:
                        rooms.append(r.id)
            queryset = queryset.filter(id__in=rooms)

        if request.POST.get('blackboard', False):
            rooms_all = Room.objects.all()
            rooms = []
            # iteruje po wszytskich pokojach
            for r in rooms_all:
                yet = False
                # i po calym sprzecie w nich
                for e in r.boards.all():
                    #jesli jest, to dorzucam do listy
                    if e.type == 'blackboard' and not yet:
                        rooms.append(r.id)
            queryset = queryset.filter(id__in=rooms)

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

    return render(request, 'a/list.html', {'queryset': queryset })