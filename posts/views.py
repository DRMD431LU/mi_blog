from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from posts.models import Post 
from django.utils.six.moves.urllib.parse import quote_plus
from .forms import PostForm
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
# Create your views here.
def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form =PostForm(request.POST or None, request.FILES or None)
	#if request.method == "POST":
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, "Tu post se ha creado :D")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form
	}
	return render(request, "post_form.html", context)
	
def post_detail(request, slug=None):
	#instance = Post.objects.get(slug=1)
	instance = get_object_or_404(Post,slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404

	share_string= quote_plus(instance.titulo)
	context={
	"titulo":instance.titulo,
	"instance":instance,
	"share_string":share_string,
	}
	return render(request,"post_detail.html",context)

def post_list(request):
	hoy = timezone.now().date()
	queryset_list = Post.objects.active() #filter(draft=False).filter(publish__lte=timezone.now())#all()#.order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	query=request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(titulo__icontains=query)|
			Q(contenido__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()
	paginator = Paginator(queryset_list, 2) # Show 25 contacts per page
	page_request_var="miau"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		contacts = paginator.page(paginator.num_pages)
	context={
		"titulo":"List",
		"object_list":queryset,
		"page_request_var":page_request_var,
		"hoy":hoy,
		}
	return render(request,"post_list.html",context)

def post_update(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"Tu <a href='#'>post</a> se ha actualizado :D", extra_tags="html_safe")
		return HttpResponseRedirect(instance.get_absolute_url())
	context={
	"titulo":"instance.titulo",
	"instance":instance,
	"form": form,
	}
	return render(request,"post_form.html",context)

def post_delete(request,slug=None):
    instance = get_object_or_404(Post, id= id)
    instance.delete()
    messages.success(request, "Tu post se ha borrado :(")
    return redirect("posts:list")
