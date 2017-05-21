from django.conf.urls import include, url
from . import views
urlpatterns = [
	url(r'^$', views.login, name='login'),
	url(r'^alta$', views.alta, name='alta'),
	url(r'^inicio$', views.index, name='index'),
	url(r'^logout$', views.peticion_logout, name='logout'),
	url(r'^panel_administrador$', views.panel_administrador, name='adminsite'),
	url(r'^panel_administrador/nuevo_local/$', views.nuevo_local, name='nuevo_local'),
	url(r'^panel_administrador/editar_local/(?P<nombreLocal>[-\w\s]+)/$', views.panel_administrador, name='editar_local'),
	url(r'^panel_administrador/nuevo_turismo/$', views.nuevo_turismo, name='nuevo_turismo'),
	url(r'^panel_administrador/editar_turismo/(?P<nombreSitio>[-\w\s]+)/$', views.panel_administrador, name='editar_turismo'),	
	url(r'^contacto$', views.contacto, name='contacto'),
	url(r'^turismo$',views.lista_turismo,name='turismo'),
	url(r'^turismo/(?P<nombreSitio>[-\w\s]+)/$',views.lugar_turismo,name='detalleTurismo'),
	url(r'^gastronomia$',views.lista_gastronomia,name='gastronomia'),
	url(r'^gastronomia/(?P<nombreLocal>[-\w\s]+)/$',views.lugar_local,name='detalleLocal'),
	url(r'^nuevo_comentario$', views.anadir_comentario, name='nuevo_comentario'),	
	url(r'^mostrar_comentarios/(?P<nombreLocal>[-\w\s]+)/$', views.mostrar_comentarios, name='mostrar_comentarios'),
	url(r'^filtrar_nombre$',views.filtrar_nombre,name='filtrar_nombre'),
]