from django.contrib import admin
from posts.models import Post
# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["titulo", "timestamp","actualizado"]
    list_display_links = ["actualizado"]
    list_filter = ["timestamp"]
    search_fields = ["titulo","contenido"]
    list_editable = ["titulo"]
    class Meta:
        model=Post
admin.site.register(Post,PostModelAdmin)

