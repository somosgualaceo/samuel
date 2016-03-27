from django.conf.urls import patterns, url

urlpatterns = patterns('demo.apps.ventas.views',
	url(r'^add/producto/$','add_product_view',name= "vista_agregar_producto"),
	url(r'^editarproducto/(?P<id_prod>.*)/$','edit_product_view',name='vista_editar_producto'),
)	