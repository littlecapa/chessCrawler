from django.urls import path

from . import views

urlpatterns = [
  # /
  path('', views.home, name='home'),
  # TEMPORARY
  path('signin', views.sign_in, name='signin'),
  path('signout', views.home, name='signout'),
  path('calendar', views.home, name='calendar'),
  path('callback', views.callback, name='callback'),
  path('config', views.config, name='config'),
]