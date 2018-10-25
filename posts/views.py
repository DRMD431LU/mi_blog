from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from posts.models import Post 
from .forms import PostForm
# Create your views here.
def post_create(request):
	form =PostForm()
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
	return render(request,"index.html",context)

def post_update(request):
    return HttpResponse("<h1>>:V</h1>")

def post_delete(request):
    return HttpResponse("<h1>>:V</h1>")