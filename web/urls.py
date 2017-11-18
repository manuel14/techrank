from django.conf.urls import url, include 
from . import views

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^seguimiento$', views.seguimiento, name='seguimiento'),
    url(r'^logout_view$', views.logout_view, name='logout'),
    url(r'^dato$', views.dato, name='dato'),
]