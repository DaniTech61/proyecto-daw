from django.conf.urls import include, url
from . import views
urlpatterns = [
	url(r'^$', views.login, name='login'),
	url(r'^alta$', views.alta, name='alta'),
	url(r'^inicio$', views.index, name='index'),
]