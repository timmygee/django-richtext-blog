from django.views.generic import ListView, DetailView

from django_blog_richtext.models import Post

class PostListView(ListView):
    """
    View functionality for a list of posts
    """
    # Define paginate_by at the url level. See urls.py
    context_object_name = 'post_list'
    queryset = Post.objects.all().order_by('-created')

class PostView(DetailView):
    """
    View functionality for a single post
    """
    model = Post
    context_object_name = 'post'
