# coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from demo.apps.ventas.models import *
from demo.apps.home.models import *
from demo.apps.home.forms import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMultiAlternatives #enviamos HTML
#paginacion en django
from django.core.paginator import Paginator, EmptyPage,InvalidPage
import json


def inicio_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			form = AuthenticationForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					return HttpResponseRedirect('/index.html')
				else:
					mensaje = "usuario y/o password incorrecto"
		form = AuthenticationForm()
		ctx = {'form':form,'mensaje':mensaje}	
		return render_to_response('home/login.html',ctx,context_instance=RequestContext(request))      

def recuperaclave_view(request):
	mensaje = ""
	value = ""
	if request.method == 'POST':
		value = request.POST['email']
		try:
			import uuid
			usuario = userProfile.objects.get(email=value)
			try:
				rescue = userRescuePassword.objects.get(user=usuario)
			except:
				rescue = userRescuePassword.objects.create(user=usuario, token=str(uuid.uuid4()))
			mensaje = "Revisa tu email para recuperar tu contraseña."
			to = usuario.email
			enlace = 'http://localhost:8000/recuperaclave/%d/%s' % (usuario.id, rescue.token)
			html_content = u"Da click en el siguiente enlace o copialo y pegalo en tu navegador para proceder a recuperar tu contraseña.<hr><a href='%(enlace)s'>%(enlace)s</a>" % {'enlace':enlace}
			msg = EmailMultiAlternatives('Recuperación de Contraseña', html_content, 'from@server.com',[to])
			msg.attach_alternative(html_content,'text/html')
			msg.send()
		except:
			mensaje = "No hay ningun usuario con este email"
	ctx = {'mensaje':mensaje, 'value':value}
	return render_to_response('home/recuperaclave.html',ctx,context_instance=RequestContext(request))

def recuperaclave2_view(request, user, token):
	rescue = get_object_or_404(userRescuePassword, user=user, token=token)
	if request.method == "POST":
		password = request.POST['password']
		usuario = userProfile.objects.get(email=rescue.user.email)
		usuario.set_password(password)
		usuario.save()
		rescue.delete()
		return HttpResponseRedirect('/login')
	ctx = {}
	return render_to_response('home/cambiapassword.html',ctx,context_instance=RequestContext(request))

def index_view(request):
	productos_mv = producto.objects.all().order_by('-visitas')[:4]
	ctx = {'productos_mv':productos_mv}
	return render_to_response('home/index.html',ctx, context_instance=RequestContext(request))

def about_view(request):
	mensaje = "Derechos Reservados 2013 - 2014"
	ctx = {'msg':mensaje}
	return render_to_response('home/about.html',ctx,context_instance=RequestContext(request))

def productos_view(request,pagina=1,user=None):
	categorias = categoria.objects.all().order_by('-id')
	ciudades = ciudad.objects.all().order_by('-id')
	try:
		categoria_get = int(request.GET.get('cat', 'c'))
	except:
		categoria_get = None
	try:
		ciudad_get = int(request.GET.get('ciu', 'c'))
	except:
		ciudad_get = None
	if request.GET.get('nombre_producto') is not None:
		options = dict(status=True, nombre__icontains=request.GET['nombre_producto'])
		if user is not None:
			options['autor__nombre'] = user
		if categoria_get is not None:
			options['categoria'] = categoria_get
		if ciudad_get is not None:
			options['ciudad'] = ciudad_get
		lista_prod = producto.objects.filter(**options).order_by('-id')
	else:
		options = dict(status=True)
		if user is not None:
			options['autor__nombre'] = user
		if categoria_get is not None:
			options['categoria'] = categoria_get
		if ciudad_get is not None:
			options['ciudad'] = ciudad_get
		lista_prod = producto.objects.filter(**options).order_by('-id')
	#lista_prod = producto.objects.filter(status=True).order_by('-id')#Selec * from ventas_productos where status = True
	paginator = Paginator(lista_prod,12)#cuantos productos quieres por pagina
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		productos = paginator.page(page)
	except (EmptyPage,InvalidPage) :
		productos = paginator.page(paginator.num_pages)   
	productos_mv = producto.objects.all().order_by('-visitas')[:4]
	try:
		ctx = {'productos_mv':productos_mv, 'request':request, 'autor':user, 'username_autor':userProfile.objects.get(nombre=user) if user else None, 'productos':productos,'categorias':categorias, 'ciudades':ciudades, 'categoria_get':categoria_get, 'ciudad_get':ciudad_get, 'query_s':request.GET.get('nombre_producto'), "num_pages":xrange(1, productos.paginator.num_pages+1)}
	except:
		return redirect('/')
	return render_to_response('home/productos.html',ctx,context_instance=RequestContext(request))

def singleProduct_view(request,id_prod):
	prod = producto.objects.get(id=id_prod)
	if request.is_ajax() and request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			nombre = form.cleaned_data.get('nombre')
			email = form.cleaned_data.get('email')
			mensaje = form.cleaned_data.get('mensaje')

			print nombre
			print email
			print mensaje

			to_mail = 'vendeazuay@gmail.com' # correo del servidor por defecto
			if prod.autor is not None:
				to_mail = prod.autor.email
			else:
				to_mail = prod.email
			my_subject, linea_separadora = 'Contácto desde ClasificadosAzuay', '-'*15
			mensaje_texto = 'De: %s <%s>\nMensaje: \n%s\n%s\n%s' % (nombre, email, mensaje, linea_separadora, linea_separadora)
			mensaje_html = '<p><b>De:</b> %s &lt;%s&gt;</p><p><b>Mensaje:</b> </p><hr><pre>%s</pre><hr>' % (nombre, email, mensaje)

			from django.core.mail.message import EmailMultiAlternatives
			msg = EmailMultiAlternatives(my_subject, mensaje_texto, 'vendeazuay@gmail.com', [to_mail])
			msg.attach_alternative(mensaje_html, 'text/html')
			msg.send()
			return HttpResponse(json.dumps({'enviado':True}), mimetype="application/json")
	else:
		form = ContactForm()
		prod = producto.objects.get(id=id_prod)
		prod.visitas += 1
		prod.save()
		productos = producto.objects.exclude(pk=prod.id).filter(categoria=prod.categoria, ciudad=prod.ciudad)[:4]
		ctx = {'producto':prod, 'relacionados':productos, 'form':form}
		return render_to_response('home/SingleProducto.html',ctx,context_instance=RequestContext(request))

def login_view(request):
		mensaje = ""
		if request.user.is_authenticated():
			return HttpResponseRedirect('/')
		else:
			if request.method == "POST":
				form = AuthenticationForm(request.POST)
				if form.is_valid:
					usuario = authenticate(username=request.POST['username'], password=request.POST['password'])
					if usuario is not None and usuario.is_active:
						login(request, usuario)
						return HttpResponseRedirect('/')
					else:
						mensaje = "usuario y/o password incorrecto"

			form = AuthenticationForm()
			ctx = {'form':form,'mensaje':mensaje}
			return render_to_response('home/login.html',ctx,context_instance=RequestContext(request))	

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def add_usuario_view(request):
	info = "Inicializando"
	if request.user.is_authenticated():
			if request.method == "POST":
					form = addUsuarioForm(request.POST)
					if form.is_valid():
						username = form.cleaned_data['usuario']
						password = form.cleaned_data['password']
						email = form.cleaned_data['email']
						p = userProfile()
						p.username = username
						p.password = password
						p.email = email
						p.save() #Guardar la informacion
						info = "Se guardo sastifactoriamente"
					else:
						info = "Informacion con datos incorrectos"
			form = addUsuarioForm()
			ctx = {'form':form,'informacion':info}	
			return render_to_response('home/addUsuario.html',ctx,context_instance=RequestContext(request))
	else: #GET
			return HttpResponseRedirect('/')
			form = addProductForm()
			ctx = {'form':form}
			return render_to_response('ventas/addProducto.html',ctx,context_instance=RequestContext(request))		

def nuevo_usuario(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')

	mensaje = 'Registro de usuario'
	if request.method == 'POST':
		formulario = NUserCreationForm(request.POST, request.FILES)
		if formulario.is_valid():
			formulario.save()
			formulario = NUserCreationForm()
			mensaje = 'Usuario registrado correctamente.'
	else:
		formulario = NUserCreationForm()
	return render_to_response('home/nuevousuario.html',{'formulario':formulario, 'mensaje':mensaje}, context_instance=RequestContext(request))

def perfil_view(request):
	if request.user.is_anonymous():
		return HttpResponseRedirect('/')

	mensaje = ''
	if request.method == 'POST':
		form1 = EditaUsuarioForm(request.POST, request.FILES, instance=request.user)
		
		mensaje = 'Actualizado con éxito'
		if len(request.POST['password']) > 0:
			if not (form1.instance.check_password(request.POST['password']) and request.POST['new_password'] == request.POST['new_password_repeat']):
				del form1.fields['password']
				del form1.fields['new_password']
				del form1.fields['new_password_repeat']
				mensaje = 'Las contraseñas no coinciden'
		else:
			del form1.fields['password']
			del form1.fields['new_password']
			del form1.fields['new_password_repeat']
			
		if form1.is_valid():
			form1.save()
			if 'password' in form1.fields:
				form1.instance.set_password(form1.cleaned_data['new_password'])
				form1.instance.save()
	
	form1 = EditaUsuarioForm(instance=request.user)
	ctx = {'form1':form1, 'mensaje':mensaje}
	return render_to_response('home/perfil.html', ctx, context_instance=RequestContext(request))