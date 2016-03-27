from django.shortcuts import render_to_response
from django.template import RequestContext
from demo.apps.ventas.forms import *
from demo.apps.ventas.models import producto,categoria
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def add_product_view(request):
	info = "Inicializando"
	if request.method == "POST":
			form = addProductForm(request.user, request.POST, request.FILES)
			if form.is_valid():
				if request.user.is_authenticated():
					p = form.save(commit=False)#Guardar la informacion
					p.autor = request.user
					p.save()
				else:
					p = form.save()
				return HttpResponseRedirect(reverse('vista_single_producto', kwargs={'id_prod':p.id}))
			else:
				info = "Informacion con datos incorrectos"
	else:
		form = addProductForm(request.user)
	ctx = {'form':form,'informacion':info, 'categorias':categoria.objects.all().order_by('-id')}
	return render_to_response('ventas/addProducto.html',ctx,context_instance=RequestContext(request))
			
def edit_product_view(request, id_prod):
	product = producto.objects.get(pk=id_prod)
	info = "Inicializando"
	if request.user.is_authenticated() and product.autor == request.user:
			if request.method == "POST":
					form = editProductForm(request.POST,request.FILES,instance=product)
					if form.is_valid():
						p = form.save(commit=False)#Guardar la informacion
						p.autor = request.user
						p.save()
						return HttpResponseRedirect('/producto/%d/' % p.id)
						#return HttpResponseRedirect(reverse('vista_agregar_producto'))
					else:
						info = "Informacion con datos incorrectos"
			else:
				form = editProductForm(instance=product)
			ctx = {'form':form,'informacion':info}
			return render_to_response('ventas/editProducto.html',ctx,context_instance=RequestContext(request))
	else: #GET
			return HttpResponseRedirect('/')