from django.conf.urls import patterns,url
from demo.apps.ventas.models import producto
from django.views.generic import ListView, DetailView

urlpatterns = patterns('demo.apps.home.views',
	url(r'^$','index_view',name='vista_principal'),
	url(r'^about/$','about_view',name='vista_about'),
	url(r'^productos/page/(?P<pagina>.*)/$','productos_view',name='vista_productos'),
	url(r'^productos/$','productos_view',name='vista_productos'),
	url(r'^productos/(?P<user>.*)/page/(?P<pagina>.*)/$','productos_view',name='vista_productos'),
	url(r'^productos/(?P<user>.*)/$','productos_view',name='vista_productos'),
	url(r'^productosadd/$','productos_view',name='vista_productos'),
	url(r'^producto/(?P<id_prod>.*)/$','singleProduct_view',name='vista_single_producto'),
	url(r'^login/$','login_view',name='vista_login'),
	url(r'^logout/$','logout_view',name='vista_logout'),
	url(r'^recuperaclave/(?P<user>\d+)/(?P<token>.*)/$','recuperaclave2_view'),
	url(r'^recuperaclave/$','recuperaclave_view',name='recuperaclave'),
	url(r'^perfil/$', 'perfil_view', name='perfil'),
	url(r'^usuario/$','add_usuario_view',name='vista_usuario'),
	url(r'^nuevousuario/$','nuevo_usuario',name='vista_nuevo_usuario'),
	url(r'^lista/$', ListView.as_view(model=producto,
				template_name='home/blog_list.html',
				paginate_by=5)
				, name="blog_list"),
	url(r'^blog/(?P<slug>[-\w]+)/$', DetailView.as_view(model=producto,
				template_name='home/blog_detail.html')
				, name="blog_detail"),               
)
