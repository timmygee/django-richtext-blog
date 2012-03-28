from django.views.generic import ListView, DetailView

from django-blog-richtext.models import Post

class PostListView(ListView):
    """
    View functionality for a list of posts
    """
    # Define paginate_by at the url level. See urls.py
    context_object_name = 'post_list'
    queryset = Post.objects.all.order_by('-created')

