from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.conf import settings

class Post(models.Model):
    """
    Defines a blog post
    """
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', max_length=50,
        editable=settings.SLUGS_EDITABLE, unique=True, blank=True,
        help_text='Leave this field blank to auto-generate slug from title')
    author = models.ForeignKey(User, related_name='post_author',
        editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', related_name='tag_posts', blank=True,
        null=True)
    content = models.TextField(blank=True)
    comments_closed = models.BooleanField(default=False,
        help_text='If ticked, this post will be closed to further comments')

    def has_edits(self):
        """
        Returns True if the post has been edited
        """
        return self.modified != self.created

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('post', (), {
            'month': self.created.strftime('%m'),
            'year': self.created.year,
            'slug': self.slug
            })

    def number_of_comments(self):
        """
        Alias for get_number_of_comments
        """
        return self.get_number_of_comments()

    def get_number_of_comments(self):
        """
        Returns a count of the number of comments
        """
        return Comment.objects.filter(post=self).count()

    def tag_list_str(self):
        """
        Returns a list of any associated tags
        """
        return u', '.join([tag.name for tag in self.tags.all()])
        

class Comment(models.Model):
    """
    Defines comments that can be stored against individual posts
    """
    post = models.ForeignKey(Post, related_name='post_comments')
    author = models.CharField(max_length=150, blank=True, verbose_name='name')
    auth_user = models.ForeignKey(User, related_name='comment_user',
        editable=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=150,
        help_text='Your email address is for authentication reasons only and '
            'will not be visible on this site')
    comment = models.TextField(help_text='Enter your comment here')

    def highlighted(self):
        """
        Indicates whether this comment was made by an authenticated user and
        the name field is unpopulated
        """
        return self.auth_user and (self.author == self.auth_user.username)

    def __unicode__(self):
        return u'Authed user: %s, name: %s' % (self.auth_user, self.author)

class Tag(models.Model):
    """
    Defines a keyword categorisation for posts
    """
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name', max_length=50,
        editable=settings.SLUGS_EDITABLE, unique=True, blank=True,
        help_text='Leave this field blank to auto-generate slug from title')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('tag', (), {'slug': self.slug})
