from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.conf import settings

class Post(models.Model):
    """
    Defines a blog post
    """
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', max_length=150,
        editable=settings.SLUGS_EDITABLE, unique=True,
        help_text='Leave this field blank to auto-generate slug from name')
    author = models.ForeignKey(User, related_name='post_author')
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def has_edits(self):
        """
        Returns True if the post has been edited
        """
        return self.modified != self.created

    def __unicode__(self):
        return self.title

