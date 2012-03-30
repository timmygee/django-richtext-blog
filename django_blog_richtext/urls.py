try:
    from django.conf.urls import patterns, include, url
except ImportError:
    from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from filebrowser.sites import site

from django_blog_richtext.views import PostListView, PostView

admin.autodiscover()

urlpatterns = patterns('',
    # 3rd party url definitions
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    # django_blog_richtext definitions
    url(r'^posts/$', PostListView.as_view(
            paginate_by=2,
            template_name='post-list.html'
        )),
    url(r'^(?P<year>[\d]{4})/(?P<month>[\d]{2})/(?P<slug>[-\w]+)/$',
        PostView.as_view(template_name='post-detail.html'), name='post'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # Serve up media files in debug mode
    )

