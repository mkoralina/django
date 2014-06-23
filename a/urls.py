from django.conf.urls import patterns, url
from a import views

urlpatterns = patterns('',
    url(r'^(?P<room_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<room_id>\d+)/make_reservation$', views.make_reservation, name='make_reservation'),
    url(r'^reserve$', views.list, name='list'),
    url(r'^login$', views.log_in, name='login'),
    url(r'^logout$', views.log_out, name='logout'),
    url(r'^database/(?P<what>\w+)/$', views.database, name='database'),
    url(r'^cache.manifest$', views.manifest, name='manifest'),
    url(r'^jquery.js$', views.jquery, name='jquery'),
    url(r'^bootstrap/css/bootstrap.min.css$', views.bootstrapcss, name='bootstrapcss'),
    url(r'^bootstrap/js/bootstrap.min.js$', views.bootstrapjs, name='bootstrapjs'),
    url(r'^jquery.min.js$', views.jquerymin, name='jquerymin'),
    url(r'^ajax-loader$', views.loader, name='loader'),
    url(r'^tests.js$', views.tests, name='tests'),
    url(r'^qunit-1.14.0.js$', views.qunitjs, name='qunitjs'),
    url(r'^qunit-1.14.0.css$', views.qunitcss, name='qunitcss'),
    url(r'^simplePagination/simplePagination.js$', views.simplejs, name='simplejs'),
    url(r'^simplePagination/simplePagination.css$', views.simplecss, name='simplecss'),

)