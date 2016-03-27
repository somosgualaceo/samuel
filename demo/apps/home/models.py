from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
	def create_user(self, email, nombre, password=None):
		nu = self.model(
			email=email,
			nombre=nombre
		)
		nu.set_password(password)
		nu.save(using=self._db)
		return nu

	def create_superuser(self, email, nombre, password):
		nsu = self.create_user(email, nombre, password)
		nsu.is_admin = True
		nsu.save(using=self._db)
		return nsu

class userProfile(AbstractBaseUser):
	def url(self,filename):
		ruta = "MultimediaData/Users/%s/%s"%(self.email,filename)
		return ruta

	email = models.EmailField(unique=True)
	nombre = models.CharField(max_length=150, unique=True, help_text='Ej: vendeazuay, jorgeortiz', verbose_name='Nombre Unico')
	foto = models.ImageField(upload_to=url, blank=True)
	telefono = models.IntegerField(max_length=30, default=0)
	direccion = models.CharField(max_length=100, default='n/a')

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['nombre']

	def __unicode__(self):
		return self.nombre

	@property
	def is_staff(self):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

	def has_perm(self, perm, obj=None):
		return True

	def get_short_name(self):
		return self.email

class userRescuePassword(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	token = models.CharField(max_length=500)

	def __unicode__(self):
		return self.token