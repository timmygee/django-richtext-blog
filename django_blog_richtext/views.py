from django.views.generic import list, detail, edit
from django.views.generic.edit import BaseFormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.base import TemplateResponseMixin

from django_blog_richtext.models import Post, Comment
from django_blog_richtext.forms import CommentForm

class PostListView(list.ListView):
    """
    View functionality for a list of posts
    """
    # Define paginate_by at the url level. See urls.py
    context_object_name = 'post_list'
    queryset = Post.objects.all().order_by('-created')

class PostView(edit.ProcessFormView, detail.DetailView, edit.FormMixin):
    """
    View for a single post
    Combintes the functionality of ProcessFormView and DetailView
    """
    model = Post
    context_object_name = 'post'
    form_class = CommentForm

    ## def get(self, request, **kwargs):
    ##     """
    ##     Merge functionality of edit.ProcessFormView.get and 
    ##     detail.BaseDetailView.get
    ##     """
    ##     # Pass both required objects to the context
    ##     context = self.get_context_data(form=form, object=self.object)
    ##     return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """
        Define required class attribute for DetailView functionality then pass
        it into the context along with any comments for the post
        """
        # From detail.DetailView.get (called just before get_context_data, so
        # we need the line here)
        self.object = self.get_object()

        # Call the parent get_context_data (in this case it will be the one
        # defined in exit.ProcessFormView)
        context = super(PostView, self).get_context_data(**kwargs)
        context['object'] = self.object
        context['comments'] = Comment.objects.filter(post=self.object)
        return context

