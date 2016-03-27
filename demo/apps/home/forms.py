# coding=utf-8
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class HTML5EmailInput(forms.widgets.Input):
	input_type = 'email'

class ContactForm(forms.Form):
	nombre = forms.CharField(widget=forms.TextInput(attrs={'required':''}))
	email = forms.EmailField(widget=HTML5EmailInput(attrs={'required':''}))	
	mensaje = forms.CharField(widget=forms.Textarea(attrs={'required':''}))

class CambiaPasswordForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput)

class EditaUsuarioForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(), label='Contraseña Actual', required=False)
	new_password = forms.CharField(widget=forms.PasswordInput(), label='Contraseña Nueva', required=False)
	new_password_repeat = forms.CharField(widget=forms.PasswordInput(), label='Contraseña Nueva (De nuevo)', required=False)

	class Meta:
		model = userProfile
		fields = ('nombre', 'password', 'new_password', 'new_password_repeat', 'email', 'telefono', 'direccion', 'foto')
		widgets = {
			'nombre': forms.TextInput(attrs={'required':'', 'pattern':'^[A-Za-z0-9]*$'}),
			'email': HTML5EmailInput(attrs={'required':''}),
			'telefono': forms.TextInput(attrs={'pattern':'^[0-9]*$'})
		}

class NUserCreationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'required':''}), label='Contraseña')

	class Meta:
		model = userProfile
		fields = ('nombre', 'password', 'email', 'telefono', 'direccion', 'foto')
		widgets = {
			'nombre': forms.TextInput(attrs={'required':'', 'pattern':'^[A-Za-z0-9]*$'}),
			'email': HTML5EmailInput(attrs={'required':''}),
			'telefono': forms.TextInput(attrs={'pattern':'^[0-9]*$'})
		}

	def save(self, commit=True):
		nu = super(NUserCreationForm, self).save(commit=False)
		nu.set_password(self.cleaned_data['password'])
		if commit: nu.save()
		return nu