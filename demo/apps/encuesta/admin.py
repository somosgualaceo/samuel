from django.contrib import admin
from demo.apps.encuesta.models import Encuesta,Respuesta



class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['pregunta']}),
        ('Date information', {'fields': ['fecha'], 'classes': ['collapse']}),
    ]



 

admin.site.register(Encuesta, PollAdmin)
admin.site.register(Respuesta)

