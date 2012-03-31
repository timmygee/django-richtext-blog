from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from django_blog_richtext.models import Post, Comment

class PostListView(ListView):
    """
    View functionality for a list of posts
    """
    # Define paginate_by at the url level. See urls.py
    context_object_name = 'post_list'
    queryset = Post.objects.all().order_by('-created')

class PostView(DetailView, FormMixin):
    """
    View functionality for a single post
    """
    model = Post
    context_object_name = 'post'

    def get_context_data(**kw):
        """
        Add to context the queryset for assiciated comments
        """
        context = super(DetailView, self).get_context_data(**kw)
        context['comments'] = Comment.
