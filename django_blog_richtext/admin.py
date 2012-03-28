from django.contrib import admin

from models import Post
from forms import PostAdminForm

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    search_fields = ('title',)

admin.site.register(Post, PostAdmin)
