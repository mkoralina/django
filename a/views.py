from django.shortcuts import render, get_object_or_404
from django.http import Http404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from a.models import Poll, Reservation, Choice
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse


def index(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]

    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'a/index.html', context)

    #template = loader.get_template('a/index.html')
    #context = RequestContext(request, {
    #    'latest_poll_list': latest_poll_list,
    #})
    #return HttpResponse(template.render(context))

#def index(request):
#    return HttpResponse("Hello, world. You're at the poll index.")    


def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'a/detail.html', {'poll': poll})


def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'a/results.html', {'poll': poll})

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
	return HttpResponse("Strona z rezerwacjami. Rezerwacja: %s." % reservation_id)