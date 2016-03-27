from django.db import models
from django.conf import settings

class categoria(models.Model):
    nombre = models.CharField(max_length=200)
    def __unicode__(self):
        return self.nombre

class ciudad(models.Model):
	nombre = models.CharField(max_length=200)
	def __unicode__(self):
		return self.nombre

class cliente(models.Model):
	nombre = models.CharField(max_length=200)
	apellidos = models.CharField(max_length=200)
	status = models.BooleanField(default=True)
	def __unicode__(self):
		nombreCompleto = "%s %s"%(self.nombre,self.apellidos)
		return nombreCompleto

class producto(models.Model):
	def url(self,filename):
		ruta = "MultimediaData/Producto/%s/%s"%(self.nombre,str(filename))
		return ruta
	fecha = models.DateTimeField(auto_now_add=True)
	categoria = models.ForeignKey(categoria, help_text='<span class="asterisc_required">*</span>')
	ciudad = models.ForeignKey(ciudad, help_text='<span class="asterisc_required">*</span>')

	nombre = models.CharField(max_length=200, help_text='<span class="asterisc_required">*</span>')
	descripcion = models.TextField(max_length=30, help_text='<span class="asterisc_required">*</span>')

	video = models.CharField(max_length=250, blank=True)

	status = models.BooleanField(default=True)
	imagen1 = models.ImageField(upload_to=url,null=True,blank=True)
	imagen2 = models.ImageField(upload_to=url,null=True,blank=True)
	imagen3 = models.ImageField(upload_to=url,null=True,blank=True)
	imagen4 = models.ImageField(upload_to=url,null=True,blank=True)
	imagen5 = models.ImageField(upload_to=url,null=True,blank=True)
	imagen6 = models.ImageField(upload_to=url,null=True,blank=True)
	precio = models.DecimalField(max_digits=8,decimal_places=2, help_text='<span class="asterisc_required">*</span> Ej: 435.99')
	visitas = models.IntegerField(default=-1)
	autor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	telefono = models.IntegerField(null=True, blank=True)
   
	def __unicode__(self):
		return self.nombre
		