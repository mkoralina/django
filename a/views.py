from django.shortcuts import render
from django.http import Http404

# Create your views here.
from django.http import HttpResponse
from a.models import Poll
from django.template import RequestContext, loader


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
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render(request, 'a/detail.html', {'poll': poll})


def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s." % poll_id)    