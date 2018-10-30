from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from posts.models import Post 
from .forms import PostForm
from django.contrib import messages
# Create your views here.
def post_create(request):
	form =PostForm(request.POST or None)
	#if request.method == "POST":
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Tu post se ha creado :D")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form
	}
	return render(request, "post_form.html", context)
	
def post_detail(request, id=None):
	#instance = Post.objects.get(id=1)
	instance = get_object_or_404(Post,id=id)
	context={
	"titulo":instance.titulo,
	"instance":instance,
	}
	return render(request,"post_detail.html",context)

def post_list(request):
	queryset = Post.objects.all()
	context={
	"titulo":"List",
	"object_list":queryset,
	}
	return render(request,"base.html",context)

def post_update(request, id=None):
	instance = get_object_or_404(Post, id= id)
	form = PostForm(request.POST or None,instance=instance)
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

def post_delete(request,id=None):
    instance = get_object_or_404(Post, id= id)
    instance.delete()
    messages.success(request, "Tu post se ha borrado :(")
    return redirect("posts:list")
