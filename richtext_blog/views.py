from django.views.generic import list, detail, edit
from django.views.generic.edit import BaseFormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.shortcuts import get_object_or_404

from richtext_blog.models import Post, Comment, Tag
from richtext_blog.forms import CommentForm

class PostListView(list.ListView):
    """
    View functionality for a list of posts
    If year and/or month are passed in as initialisation kwargs then the
    queryset will be filtered based on that criteria
    """
    # Define paginate_by at the url level. See urls.py
    context_object_name = 'post_list'

    def get_queryset(self):
        """
        Return posts based on a particular year and month. 
        """
        if 'month' in self.kwargs:
            objects = Post.objects.filter(created__year=self.kwargs['year'],
                created__month=self.kwargs['month'])
        elif 'year' in self.kwargs:
            objects = Post.objects.filter(created__year=self.kwargs['year'])
        else:
            objects = Post.objects.all()
        if not objects:
            raise Http404
        return objects

    def get_context_data(self, **kwargs):
        """
        Pass up the time values. Also pass up that the view display mode is
        'monthly' or yearly if that is the case'
        """
        context = super(PostListView, self).get_context_data(**kwargs)
        if self.kwargs:
            context.update(self.kwargs)
            if 'month' in self.kwargs:
                context['display_mode'] = 'monthly'
            elif 'year' in self.kwargs:
                context['display_mode'] = 'yearly'
        return context

class TagView(PostListView):
    """
    Extend the PostListView for the functionality behind the displaying of posts
    by tag. Actual template to use is defined in accompanying urls.py (should
    use the same as the template for PostListView, or at least use similar
    functionality)
    """
    context_object_name = 'post_list'

    def get_queryset(self):
        """
        Return the queryset of posts for the currently viewed tag
        """
        return Post.objects.filter(
            tags__slug=self.kwargs['slug']).order_by('-created')

    def get_context_data(self, **kwargs):
        """
        Pass the tag object into the request object as well
        """
        context = super(TagView, self).get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, slug=self.kwargs['slug'])
            
        return context

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
        if form_data['author']:
            name = form_data['author']

        Comment.objects.create(post=self.get_object(), author=name,
            auth_user=user, email=form_data['email'],
            comment=form_data['comment'])

        messages.success(self.request, 'Comment added')
        return HttpResponseRedirect(self.get_success_url())
        
    def get_success_url(self):
        """
        Comments form processing.
        """
        return self.get_object().get_absolute_url()

