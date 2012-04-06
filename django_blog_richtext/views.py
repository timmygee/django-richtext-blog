from django.views.generic import list, detail, edit
from django.views.generic.edit import BaseFormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.contrib import messages

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
    Combines the functionality of ProcessFormView and DetailView
    Form functionality is for handling the submission of comments
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
        context['comments'] = \
            Comment.objects.filter(post=self.object).order_by('created')
        return context

    def form_valid(self, form):
        """
        Called when form is valid. Create a new comment based on form input then
        redirect to success url.
        """
        form_data = form.cleaned_data

        user = self.request.user

        # Auto set username as name if user logged in.
        if not isinstance(user, AnonymousUser):
            name = user.username
        else:
            name = 'Anonymous'
            user = None

        # Override name if submitted in form
        if form_data['name']:
            name = form_data['name']

        Comment.objects.create(post=self.get_object(), name=name, auth_user=user,
            email=form_data['email'], comment=form_data['comment'])

        messages.success(self.request, 'Comment added')
        return HttpResponseRedirect(self.get_success_url())
        
    def get_success_url(self):
        """
        Comments form processing.
        """
        return self.get_object().get_absolute_url()

