try:
    from django.conf.urls import patterns, include, url
except ImportError:
    from django.conf.urls.defaults import patterns, include, url

from richtext_blog.views import (PostListView, PostView, TagView,
    AllPostsRssFeed, AllPostsAtomFeed, RedirectToPostsView)

urlpatterns = patterns('',
    url(r'^$', RedirectToPostsView.as_view(permanent=True)),
    url(r'^posts/$', PostListView.as_view(
        paginate_by=10,
        template_name='post-list.html',
        ), name='posts_all'),
    url(r'^(?P<year>[\d]{4})/$', PostListView.as_view(
        paginate_by=10,
        template_name='post-list.html',
        ), name='posts_yearly'),
    url(r'^(?P<year>[\d]{4})/(?P<month>[\d]{2})/$', PostListView.as_view(
        paginate_by=10,
        template_name='post-list.html',
        ), name='posts_monthly'),
    url(r'^(?P<year>[\d]{4})/(?P<month>[\d]{2})/(?P<slug>[-\w]+)/$',
        PostView.as_view(template_name='post-detail.html'), name='post'),
    url(r'^tags/(?P<slug>[-\w]+)/$', TagView.as_view(
        template_name='tag-view.html'), name='posts_tag'),
    url(r'^rss/$', AllPostsRssFeed(), name='posts_all_rss'),
    url(r'^atom/$', AllPostsAtomFeed(), name='posts_all_atom')
    )

