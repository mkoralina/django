from django.conf.urls import patterns, url
from a import views

urlpatterns = patterns('',
    url(r'^(?P<room_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<room_id>\d+)/make_reservation$', views.make_reservation, name='make_reservation'),
    url(r'^reserve$', views.list, name='list'),
    url(r'^login$', views.log_in, name='login'),
    url(r'^logout$', views.log_out, name='logout'),
    url(r'^database/(?P<what>\w+)/$', views.database, name='database'),
)