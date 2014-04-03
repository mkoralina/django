from django.conf.urls import patterns, url

from a import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    url(r'^reserve$', views.list, name='list'),
    url(r'^reserve/(?P<reservation_id>\d+)/$', views.reserve, name='reserve'),
    url(r'^login$', views.log_in, name='login'),
    url(r'^logout$', views.log_out, name='logout'),

)