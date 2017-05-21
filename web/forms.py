from django import forms
from django.contrib.auth.models import User
from .models import Local,Turismo,Comentarios
from django.forms import ModelForm,CharField,Form,PasswordInput

class AltaForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password', 'email', 'first_name', 'last_name']
		widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
			'username': forms.TextInput(attrs={'class': 'form-control'}),
			'email': forms.TextInput(attrs={'class': 'form-control'}),
			'first_name': forms.TextInput(attrs={'class': 'form-control'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
		
class LoginForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']
		widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
			'username': forms.TextInput(attrs={'class': 'form-control'}),			
        }
		
class FiltroTurismoForm(forms.Form):
	class Meta:
		model = Turismo
	CATEGORIAS_TURISMO = (
		('---', '---'),
		('fuente', 'Fuente'),
		('parque', 'Parque'),
		('museo', 'Museo'),
		('teatro', 'Teatro'),
		('auditorio', 'Auditorio'),	
		('puerta', 'Puerta'),
		('otros', 'Otros'),
	)
	select = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'onChange':'form.submit();'}), choices=CATEGORIAS_TURISMO)
		
		
class FiltroLocalForm(forms.Form):
	class Meta:
		model = Local
	CATEGORIAS_LOCALES = (
		('---', '---'),
		('noche', 'Noche'),
		('comer', 'Comer'),
		('tapeo', 'Tapas'),
		('dulce', 'Dulce'),
		('varios', 'Varios'),
	)
	select = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'onChange':'form.submit();'}), choices=CATEGORIAS_LOCALES)

class ComentarioForm(ModelForm):
	class Meta:
		model = Comentarios
		fields = ('titulo', 'comentario')
		widgets = {
			'titulo': forms.TextInput(attrs={'class': 'form-control'}),
			'comentario': forms.Textarea(attrs={'class': 'form-control'}),
        }

class FormularioContacto(forms.Form):
    mensaje = forms.CharField(widget=forms.Textarea, required=True)
	
class NuevoTurismoForm(ModelForm):
	class Meta:
		model = Turismo
		fields = ['nombreSitio', 'direccion', 'descripcion','categoria']
		widgets ={
			'nombreSitio' : forms.TextInput(attrs={'class': 'form-control'}),
			'direccion' : forms.TextInput(attrs={'class': 'form-control'}),
			'descripcion' : forms.Textarea(attrs={'class': 'form-control'}),
		}
		categoria = forms.ChoiceField(choices=Turismo.CATEGORIAS_TURISMO),

class NuevoLocalForm(ModelForm):
	class Meta:
		model = Local
		fields = ['nombreLocal', 'direccion', 'descripcion','categoria','telefono','email','web']
		widgets ={
			'nombreLocal' : forms.TextInput(attrs={'class': 'form-control'}),
			'direccion' : forms.TextInput(attrs={'class': 'form-control'}),
			'descripcion' : forms.Textarea(attrs={'class': 'form-control'}),
			'telefono' : forms.TextInput(attrs={'class': 'form-control'}),
			'email' : forms.EmailInput(attrs={'class': 'form-control'}),
			'web' : forms.URLInput(attrs={'class': 'form-control'}),
		}
		categoria = forms.ChoiceField(choices=Local.CATEGORIAS_LOCALES),