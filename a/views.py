from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import datetime
from django.core import serializers
import json
import json as simplejson

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

        hours = request.POST.getlist('hours[]')

        try:

            if len(hours) > 0:

                room = Room.objects.select_for_update().get(id=room_id)
                terms_id = []


                #try:
                for i in range (0, len(hours)):

                    start = int(hours[i])

                    end = int(hours[i]) + 1

                    #raise StandardError("tutaj")

                    begin_time = datetime.strptime(str(start), "%H").time()
                    end_time = datetime.strptime(str(end), "%H").time()

                    for t in room.terms.all():
                        terms_id.append(t.id)

                    #raise StandardError("{0} - {1} w roomie:{2}".format(terms_id,t.end_time, room.id))
                    try:
                        term = Term.objects.select_for_update().get(begin_time__lte=begin_time, end_time__gte=end_time, date=date, id__in=terms_id)
                   # term = Term.objects.select_for_update().filter(Q(begin_time__lte=begin_time) |
                   #                                                Q(end_time__gte=end_time) |
                   #                                                Q(date=date) |
                   #                                                Q(id__in=terms_id))



                    except:
                        raise StandardError("termin nie znaleziony dla {0} - {1} dnia {2} i pokoju: {4} w terminach: {3} o id: {5}".format(start, end, date, room.terms.all(),room_id, terms_id))

                    #except(Term.DoesNotExist, Room.DoesNotExist):
                    #    return render(request, 'a/make_reservation.html',
                    #          {'error_message': 'We are sorry, the term you wanted to '
                    #                            'reserve is no longer available.'})

                    r = Reservation()


                    #r.room = room
                    #r.user = request.user
                    #r.term = term[0]
                    #r.save()

                    term = r.prepare_term(begin_time, end_time, term, room)
                    r.reserve(room, term, request.user)

                    del terms_id[0:len(terms_id)]

        except:
            raise StandardError("Impossible to reserve")

    #update bazy danych na stronie
    rooms = Room.objects.all()
    rooms = serializers.serialize('json',rooms)
    terms = Term.objects.all()
    terms = serializers.serialize('json',terms)
    r = simplejson.dumps({"rooms": rooms, "terms": terms})
    return HttpResponse(r)





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



def database(request, what):
    items = []
    if what == 'rooms':
        items = Room.objects.all()
    elif what == 'terms':
        items = Term.objects.all()
    elif what == 'equip':
        items = Equipment.objects.all()
    elif what == 'boards':
        items = Board.objects.all()

    data = serializers.serialize('json',items)

    return HttpResponse(data)


def manifest(request):
    return render(request, 'a/offline/cache.manifest', content_type='text/manifest')

def csrf(request):
    return render(request, 'a/offline/csrf.js', content_type='text/javascript')

def jquery(request):
    return render(request, 'a/offline/jquery.js', content_type='text/javascript')

def jquerymin(request):
    return render(request, 'a/offline/jquery.min.js', content_type='text/javascript')

def bootstrapcss(request):
    return render(request, 'a/offline/bootstrap/css/bootstrap.min.css', content_type='text/css')

def bootstrapjs(request):
    return render(request, 'a/offline/bootstrap/js/bootstrap.min.js', content_type='text/javascript')

def loader(request):
    return render(request, 'a/offline/loader.gif', content_type='image/gif')


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