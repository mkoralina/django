from django.conf.urls import patterns, url

from a import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)