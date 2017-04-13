from django import forms
from django.contrib.auth.models import User
from .models import Local,Turismo
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
