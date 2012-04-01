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
    View functionality for a single post
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
        Define required class attributed for both DetailView and ProcessFormView
        then pass them into the context
        """
        # From edit.ProcessFormView.get
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # From detail.DetailView.get
        self.object = self.get_object()

        context = super(PostView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        context['form'] = form
        context['object'] = self.object
        return context

