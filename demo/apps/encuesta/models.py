from django.db import models
import datetime
from django.utils import timezone

class Encuesta(models.Model):
 pregunta = models.CharField(max_length=200)
 fecha = models.DateTimeField('Fecha Publicacion')
 def __unicode__(self):
	return self.pregunta
 def fecha_hoy(self):
	return self.fecha >= timezone.now() - datetime.timedelta(days=1)
	
class Respuesta(models.Model):
 encuesta = models.ForeignKey(Encuesta)
 respuesta = models.CharField(max_length=200)
 voto = models.IntegerField()
 def __unicode__(self):
	return self.respuesta

