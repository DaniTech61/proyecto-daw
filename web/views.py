from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login
from web.forms import AltaForm
from web.forms import LoginForm
from web.forms import FiltroTurismoForm
from web.forms import FiltroLocalForm
from web.forms import ComentarioForm
from web.forms import FormularioContacto
from web.forms import NuevoTurismoForm
from web.forms import NuevoLocalForm
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Local
from .models import Turismo
from .models import Comentarios
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import os.path
from django.core.urlresolvers import resolve

# Create your views here.
@ensure_csrf_cookie
def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth_login(request, user)
				if user.groups.filter(name='Editores').exists():
					return render(request,'web/administrador/index.html')
				else:
					return render(request,'web/index.html')
	else:
		form = LoginForm()

	data = {
		'form': form,
	}
	return render(request,'web/login.html',data)

def peticion_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('login'))


@ensure_csrf_cookie	
def alta(request):
	if request.method == 'POST':  # If the form has been submitted...
		form = AltaForm(request.POST)  # A form bound to the POST data
		if form.is_valid():  # All validation rules pass
			# Process the data in form.cleaned_data
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			email = form.cleaned_data["email"]
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]
			# At this point, user is a User object that has already been saved
			# to the database. You can continue to change its attributes
			# if you want to change other fields.
			user = User.objects.create_user(username, email, password)
			user.first_name = first_name
			user.last_name = last_name
			# Save new user attributes
			user.save()
			return HttpResponseRedirect(reverse('login'))  # Redirect after POST
	else:
		form = AltaForm()

	data = {
		'form': form,
	}
	return render(request,'web/alta.html', data)
	

def index(request):
	if request.user.is_authenticated():
		return render(request,'web/index.html', {'user': request.user})
	else:
		return render(request,'web/login.html')
    
	
def lista_turismo(request):
	page = request.GET.get('page')
	lista_turismo = ""
	filtro = ""
	nombres = Turismo.objects.values("nombreSitio")
	
	if request.method == 'POST':
		if request.POST.get('Borrar'):
			if 'filtroTurismo' in request.session:
				del request.session['filtroTurismo']		
		else:
			filtro=request.POST.get('select') 
			request.session['filtroTurismo'] = filtro

	if 'filtroTurismo' not in request.session:
		lista_turismo = Turismo.objects.order_by('nombreSitio')
	else:
		lista_turismo = Turismo.objects.filter(categoria=request.session['filtroTurismo'])
		
	paginator = Paginator(lista_turismo, 6)
	try:
		turismo=paginator.page(page)
	except PageNotAnInteger:
		turismo=paginator.page(1)
	except EmptyPage:
		turismo=paginator.page(paginator.num_pages)
		
	form = FiltroTurismoForm()	
	data = {
		'form': form,
		'turismo': turismo, 
		'filtro': filtro,
		'nombres': nombres,
	}	
	return render(request, 'web/turismo.html', data)

def lugar_turismo(request,nombreSitio):
	turismo = Turismo.objects.get(nombreSitio=nombreSitio)
	data = {
		'sitio':turismo,
	}
	return render(request, 'web/turismo/turismo.html',data)
	
def lista_gastronomia(request):
	page = request.GET.get('page')
	lista_local = ""
	filtro = ""
	nombres = Local.objects.values("nombreLocal")
	
	if request.method == 'POST':
		if request.POST.get('Borrar'):
			if 'filtroLocal' in request.session:
				del request.session['filtroLocal']		
		else:
			filtro=request.POST.get('select') 
			request.session['filtroLocal'] = filtro

	if 'filtroLocal' not in request.session:
		lista_local = Local.objects.order_by('nombreLocal')
	else:
		lista_local = Local.objects.filter(categoria=request.session['filtroLocal'])
		
	paginator = Paginator(lista_local, 6)
	try:
		locales=paginator.page(page)
	except PageNotAnInteger:
		locales=paginator.page(1)
	except EmptyPage:
		locales=paginator.page(paginator.num_pages)
		
	form = FiltroLocalForm()	
	data = {
		'form': form,
		'locales': locales, 
		'filtro': filtro,
		'nombres': nombres,
	}	
	return render(request, 'web/gastronomia.html', data)
	
def lugar_local(request,nombreLocal):
	local = Local.objects.get(nombreLocal=nombreLocal)
	formComentario = ComentarioForm()	
	data = {
		'formComentario':formComentario,
		'sitio':local,
	}
	return render(request, 'web/local/local.html',data)
	
def anadir_comentario(request):
	local = Local.objects.get(nombreLocal=request.POST.get('local'))
	if request.method == 'POST':
		form = ComentarioForm(request.POST)
		if form.is_valid():
			comentario = Comentarios(
				titulo=form.cleaned_data["titulo"],
				comentario=form.cleaned_data["comentario"],
				autor = request.user,
				fecha_publicacion = timezone.now(),
				local=local
			)
			comentario.save()
	comentarios = Comentarios.objects.filter(local=local)
	return mostrar_comentarios(request,local.nombreLocal)
	
			
def mostrar_comentarios(request,nombreLocal):
	local = Local.objects.get(nombreLocal=nombreLocal)
	comentarios = Comentarios.objects.filter(local=local)	
	data = {
		'comentarios': comentarios,
	}	
	return render(request, 'web/comentarios.html', data)
	
@ensure_csrf_cookie	
def contacto(request):
	if request.method == 'POST':	
		form = FormularioContacto(request.POST)
		if form.is_valid():
			usuario = request.user.get_full_name()
			user = User.objects.get(username=request.user.username)
			from_email = user.email
			mensaje = form.cleaned_data['mensaje'] + "<br>" + from_email
			msg = EmailMessage(usuario,mensaje,from_email,['correopruebasdaw2017@gmail.com'])
			msg.content_subtype = "html"
			msg.send()
			data = {
				'mensaje': "Mensaje enviado correctamente, gracias por ponerte en contacto",
			}
			return render(request,'web/contacto.html',data)
	else:
		form = FormularioContacto()
	data = {
		'form': form,
	}
	return render(request,'web/contacto.html',data)
	
def panel_administrador(request):
	return render(request,'web/administrador/index.html')

@ensure_csrf_cookie		
def filtrar_nombre(request):
	nombre=request.POST.get('busqueda')
	referer = request.META.get('HTTP_REFERER')
	if referer.find("gastronomia") != -1:
		local=Local.objects.filter(nombreLocal__icontains=nombre).order_by('nombreLocal').first()
		if local:
			return lugar_local(request,local.nombreLocal)
		else:
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	elif referer.find("turismo") != -1:
		turism=Turismo.objects.filter(nombreSitio__icontains=nombre).order_by('nombreSitio').first()
		if turism:
			return lugar_turismo(request,turism.nombreSitio)
		else:
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@ensure_csrf_cookie			
def nuevo_turismo(request):
	if request.method == 'POST' and request.FILES['image']:	
		form = NuevoTurismoForm(request.POST)
		if form.is_valid():
			folder = '/static/images/turismo/'
			uploaded_filename = request.FILES['image'].name
			BASE_PATH = os.path.abspath(os.path.dirname(__file__))
			full_filename = BASE_PATH+folder+uploaded_filename
			fout = open(full_filename, 'wb+')
			file_content = ContentFile( request.FILES['image'].read() )
			try:
				# Iterate through the chunks.
				for chunk in file_content.chunks():
					fout.write(chunk)
				fout.close()				
				turismo = Turismo(
					nombreSitio=form.cleaned_data["nombreSitio"],
					direccion=form.cleaned_data["direccion"],
					descripcion=form.cleaned_data["descripcion"],
					imagen="/images/turismo/"+uploaded_filename,
					categoria=form.cleaned_data["categoria"],
					fechaAlta = timezone.now(),
				)
				turismo.save()						
				mensaje = "Nuevo sitio de turismo creado correctamente"
				return render(request,'web/administrador/index.html',{'mensaje':mensaje})
			except:
				mensaje = "No se ha podido crear"
				return render(request,'web/administrador/index.html',{'mensaje':mensaje})				
	form = NuevoTurismoForm()
	return render(request,'web/administrador/forms/nuevo_turismo.html',{'form':form})

@ensure_csrf_cookie			
def nuevo_local(request):
	if request.method == 'POST' and request.FILES['image']:	
		form = NuevoLocalForm(request.POST)
		if form.is_valid():
			folder = '/static/images/gastro/'
			uploaded_filename = request.FILES['image'].name
			BASE_PATH = os.path.abspath(os.path.dirname(__file__))
			full_filename = BASE_PATH+folder+uploaded_filename
			fout = open(full_filename, 'wb+')
			file_content = ContentFile( request.FILES['image'].read() )
			try:
				# Iterate through the chunks.
				for chunk in file_content.chunks():
					fout.write(chunk)
				fout.close()				
				local = Local(
					nombreLocal=form.cleaned_data["nombreLocal"],
					direccion=form.cleaned_data["direccion"],
					descripcion=form.cleaned_data["descripcion"],
					imagen="/images/gastro/"+uploaded_filename,
					categoria=form.cleaned_data["categoria"],
					telefono=form.cleaned_data["telefono"],
					email=form.cleaned_data["email"],
					web=form.cleaned_data["web"],
					fechaAlta = timezone.now(),
				)
				local.save()						
				mensaje = "Nuevo local creado correctamente"
				return render(request,'web/administrador/index.html',{'mensaje':mensaje})
			except:
				mensaje = "No se ha podido crear"
				return render(request,'web/administrador/index.html',{'mensaje':mensaje})				
	form = NuevoLocalForm()
	return render(request,'web/administrador/forms/nuevo_local.html',{'form':form})
	
def lista_locales(request):
	lista = Local.objects.order_by('nombreLocal')
	return render(request,'web/administrador/lista/lista.html',{'lista':lista})
	
def editar_local(request,nombreLocal):
	mensaje=""
	local = Local.objects.get(nombreLocal=nombreLocal)
	form = NuevoLocalForm(instance=local)	
	if request.method == 'POST':
		form = NuevoLocalForm(request.POST,instance=local)
		if form.is_valid():
			local.nombreLocal=form.cleaned_data["nombreLocal"]
			local.direccion=form.cleaned_data["direccion"]
			local.descripcion=form.cleaned_data["descripcion"]
			local.categoria=form.cleaned_data["categoria"]
			local.telefono=form.cleaned_data["telefono"]
			local.email=form.cleaned_data["email"]
			local.web=form.cleaned_data["web"]
			local.save();
			mensaje="Local actualizado"
			local = Local.objects.get(nombreLocal=form.cleaned_data["nombreLocal"])		
	data = {
		'form':form,
		'sitio':local,
		'mensaje':mensaje,
	}
	return render(request, 'web/administrador/editar/local.html',data)

def editar_imagen_local(request,nombreLocal):
	local = Local.objects.get(nombreLocal=nombreLocal)
	os.remove(os.path.abspath(os.path.dirname(__file__))+'/static/'+local.imagen)
	if request.method == 'POST' and request.FILES['image']:	
		folder = '/static/images/gastro/'
		uploaded_filename = request.FILES['image'].name
		BASE_PATH = os.path.abspath(os.path.dirname(__file__))
		full_filename = BASE_PATH+folder+uploaded_filename
		fout = open(full_filename, 'wb+')
		file_content = ContentFile( request.FILES['image'].read() )
		try:
			# Iterate through the chunks.
			for chunk in file_content.chunks():
				fout.write(chunk)
			fout.close()				
			image="images/gastro/"+uploaded_filename
			Local.objects.filter(nombreLocal=nombreLocal).update(imagen=image)									
			return redirect(editar_local,{'nombreLocal':nombreLocal})
		except:
			mensaje = "No se ha podido crear"
			return redirect(editar_local,nombreLocal=nombreLocal)

def lista_turism(request):
	lista = Turismo.objects.order_by('nombreSitio')
	return render(request,'web/administrador/lista/lista.html',{'lista':lista})
	
def editar_turismo(request,nombreSitio):
	mensaje=""	
	turismo = Turismo.objects.get(nombreSitio=nombreSitio)	
	form = NuevoTurismoForm(instance=turismo)
	if request.method == 'POST':	
		form = NuevoTurismoForm(request.POST, instance=turismo)
		if form.is_valid():
			turismo = Turismo.objects.get(nombreSitio=nombreSitio)	
			turismo.nombreSitio=form.cleaned_data["nombreSitio"]
			turismo.direccion=form.cleaned_data["direccion"]
			turismo.descripcion=form.cleaned_data["descripcion"]
			turismo.categoria=form.cleaned_data["categoria"]
			turismo.save()				
			mensaje="Turismo actualizado"
	data = {
		'form':form,
		'sitio':turismo,
		'mensaje':mensaje,
	}
	return render(request, 'web/administrador/editar/turismo.html',data)

def editar_imagen_turismo(request,nombreSitio):
	turismo = Turismo.objects.get(nombreSitio=nombreSitio)
	os.remove(os.path.abspath(os.path.dirname(__file__))+'/static/'+turismo.imagen)
	if request.method == 'POST' and request.FILES['image']:	
		folder = '/static/images/turismo/'
		uploaded_filename = request.FILES['image'].name
		BASE_PATH = os.path.abspath(os.path.dirname(__file__))
		full_filename = BASE_PATH+folder+uploaded_filename
		fout = open(full_filename, 'wb+')
		file_content = ContentFile( request.FILES['image'].read() )
		try:
			# Iterate through the chunks.
			for chunk in file_content.chunks():
				fout.write(chunk)
			fout.close()				
			image="images/turismo/"+uploaded_filename
			Turismo.objects.filter(nombreSitio=nombreSitio).update(imagen=image)									
			return redirect(editar_local,{'nombreSitio':nombreSitio})
		except:
			mensaje = "No se ha podido crear"
			return redirect(editar_turismo,nombreSitio=nombreSitio)

def eliminar_local(request,nombreLocal):
	Local.objects.filter(nombreLocal=nombreLocal).delete()
	mensaje = "Local "+nombreLocal+" eliminado"
	return render(request,'web/administrador/index.html',{'mensaje':mensaje})

def eliminar_turismo(request,nombreSitio):
	Turismo.objects.filter(nombreSitio=nombreSitio).delete()
	mensaje = "Sitio "+nombreSitio+" eliminado"
	return render(request,'web/administrador/index.html',{'mensaje':mensaje})