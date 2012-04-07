from django.contrib import admin

from models import Post, Comment, Tag
from forms import PostFormAdmin

class CommentInline(admin.TabularInline):
    """
    Inline definition for comments
    """
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    form = PostFormAdmin
    fields = ('title', 'slug', 'tags', 'content')
    search_fields = ('title',)
    list_display = ('title', 'author', 'created', 'modified', 'tag_list')
    list_filter = ('author__username', 'tags')
    inlines = (CommentInline,)

    def save_model(self, request, obj, form, change):
        """
        Override save_model method to allow automatic population of the author
        field with the current user
        """
        obj.author = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        """
        Save changed inline objects (ie Comments)
        This is so if the logged in user saves a comment in the admin interface
        the user can be logged against the Comment object.
        """
        instances = formset.save(commit=False)
        # Instances is a list of new or changed objects. We're expecting just
        # Comment objects in the list but we will check the type in case of
        # future code modifications
        for instance in instances:
            if isinstance(instance, Comment):
                instance.auth_user = request.user
            instance.save()

admin.site.register(Post, PostAdmin)

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag, TagAdmin)
