from django.views.generic import ListView, DetailView

from django-blog-richtext.models import Post

class PostListView(ListView):
    """
    View functionality for a list of posts
    """
    model = Post
    paginate_by = 10
    context_object_name = 'post_list'

    
