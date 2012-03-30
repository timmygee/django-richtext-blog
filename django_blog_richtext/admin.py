from django.contrib import admin

from models import Post
from forms import PostFormAdmin

class PostAdmin(admin.ModelAdmin):
    form = PostFormAdmin
    search_fields = ('title',)
    list_display = ('title', 'author', 'created', 'modified')
    list_filter = ('author__first_name',)

    def save_model(self, request, obj, form, change):
        """
        Override save_model method to allow automatic population of the author
        field with the current user
        """
        obj.author = request.user
        obj.save()

admin.site.register(Post, PostAdmin)
