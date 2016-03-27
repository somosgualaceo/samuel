from django.contrib import admin
from demo.apps.ventas.models import *

#registramos los modelos de venta
admin.site.register(cliente)
admin.site.register(producto)
admin.site.register(categoria)
admin.site.register(ciudad)


