from django import forms
from django.contrib.auth.models import User
from demo.apps.ventas.models import *
from django.template import defaultfilters

class HTML5EmailInput(forms.widgets.Input):
	input_type = 'email'

class addProductForm(forms.ModelForm):
	nombre = forms.CharField(label='Titulo del anuncio', help_text='<span class="asterisc_required">*</span>', widget=forms.TextInput(attrs={'required':''}))
	video = forms.CharField(help_text='Ej: http://www.youtube.com/watch?v=vGs1kl', required=False, widget=forms.TextInput(attrs={'pattern':'^(http|https)://(www\.)?youtube\.com/watch\?v=.+$'}))

	def __init__(self, user, *args, **kwargs):
		super(addProductForm, self).__init__(*args, **kwargs)
		if user.is_anonymous():
		 	self.fields['email'] = forms.EmailField(widget=HTML5EmailInput(attrs={'required':''}), help_text='<span class="asterisc_required">*</span>')
			self.fields['telefono'] = forms.CharField(widget=forms.TextInput(attrs={'required':'', 'pattern':'[0-9]+'}), help_text='<span class="asterisc_required">*</span>')
		else:
			self.fields.pop('email')
			self.fields.pop('telefono')

	def clean_video(self):
		url = self.cleaned_data['video']
		if len(url) > 0:
			params = url.split('?v=', 1)
			codigo = params[1].split('&', 1)[0]
			return codigo
		else:
			return ''

	class Meta:
		model = producto
		widgets = {
			'categoria': forms.HiddenInput(attrs={'id':'categoria'}),
			'descripcion': forms.Textarea(attrs={'required':''}),
			'precio': forms.TextInput(attrs={'required':'', 'pattern':'[0-9]+\.?[0-9]*'}),
			'imagen2': forms.FileInput(attrs={'class':'imagenes_add_producto'}),
			'imagen3': forms.FileInput(attrs={'class':'imagenes_add_producto'}),
			'imagen4': forms.FileInput(attrs={'class':'imagenes_add_producto'}),
			'imagen5': forms.FileInput(attrs={'class':'imagenes_add_producto'}),
			'imagen6': forms.FileInput(attrs={'class':'imagenes_add_producto'}),
			'imagen7': forms.FileInput(attrs={'class':'imagenes_add_producto'}),
			'imagen8': forms.FileInput(attrs={'class':'imagenes_add_producto'})
		}
		exclude = ('status', 'visitas', 'autor')

class editProductForm(forms.ModelForm):
	class Meta:
		model = producto
		widgets = {
			'categoria': forms.Select(attrs={'id':'categoria'})
		}
		exclude = ('visitas', 'autor')