from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from web.forms import AltaForm
from web.forms import LoginForm
from django.views.decorators.csrf import ensure_csrf_cookie

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
				return render(request,'web/index.html')
	else:
		form = LoginForm()

	data = {
		'form': form,
	}
	return render(request,'web/login.html',data)	
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
    