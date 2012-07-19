====================
Django Richtext Blog
====================

Features
========

* Rich text editing implemented with TinyMCE
* Full inline image upload support via TinyMCE using grapelli and filebrowser
  modules
* Automatic image scales for posts
* Support for post tagging
* Support for comments in posts
* Code syntax highlighting with pygments
* Comment spam prevention through integration with django-simple-captcha
* Atom and RSS feed support
* Templates included to provide examples of how django-richtext-blog can be
  used
* SEO optimised urls for posts and tags

Getting Started
===============

Included is all the templates the blog system uses to display posts, tags etc.

If you're familiar enough with django you might be able to jump straight in, 
otherwise below are the steps to get it up and running in its most basic form.

The author uses this app to implement his own blog therefore a working
example can be found in the wild here http://www.wholebaked.com.au/blog/posts/

For bug reports or the latest bleeding edge version go to the GitHub project
page https://github.com/timmygee/django-richtext-blog

Installing
----------

By far the simplest way to install the latest stable vesrion is to use pip or
easy_install::

    $ pip install django-richtext-blog

This will pull in any missing package dependencies also.

Next step is to set up a django site that will use the blog app.

Currently **django-richtext-blog** requires **django 1.3** to work correctly
due to the fact that it uses **django-filebrowser** to implement inline image
uploads. Perhaps one day **django-filebrowser** will be taken to
**django 1.4** and then this package in turn can be upgraded.

**django-filebrowser** also currently requires **django-grapelli** for its
implementation of features on the admin pages. There is a version of
**django-filebrowser** that does not use **django-grapelli**
(http://pypi.python.org/pypi/django-filebrowser-django13 ) but is as yet 
untested with this app. The below instructions assume the inclusion of
**django-grapelli**.

Assuming that django is installed you should have the ``django-admin.py``
script in the system path. Set up a new site project::

    $ django-admin.py startproject myblogsite

Next configure your project to use the blog app and its dependencies by editing
``myblogsite/settings.py``. For a full explanation of these steps see the
django tutorial documentation at 
https://docs.djangoproject.com/en/1.3/intro/tutorial01/

At the top of ``settings.py`` add the lines::

    import os
    PROJECT_HOME=os.path.dirname(os.path.realpath(__file__))

Make sure you set up your database and admin log in preferences while you're
there.

Update the ``MEDIA_URL`` line to read::

    MEDIA_URL = '/media/'

Update ``STATIC_ROOT`` to::

    STATIC_ROOT = os.path.join(PROJECT_HOME, 'static')

Update ``ADMIN_MEDIA_PREFIX`` to::

    ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'

In the ``INSTALLED_APPS`` setting add ``tinymce``, ``grappelli.dashboard``,
``grappelli``, ``filebrowser`` and ``captcha`` before the entry for
``django.contrib.admin``. Make sure the ``django.contrib.admin`` line is
un-commented as well. After ``django.contrib.admindocs`` add an entry for
``richtext_blog``. The resulting ``INSTALLED_APPS`` setting might look like::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'tinymce',
        'grappelli.dashboard',
        'grappelli',
        'filebrowser',
        'captcha',
        # Uncomment the next line to enable the admin:
        'django.contrib.admin',
        # Uncomment the next line to enable admin documentation:
	'django.contrib.admindocs',
        'richtext_blog'
    	)

Add a ``TEMPLATE_CONTEXT_PROCESSORS`` setting and make sure it looks like::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.csrf',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
        # django-richtext-blog context processors
        'richtext_blog.context_processors.blog_global'
        )

Add the below lines to the bottom of the ``settings.py`` file to implement
some default settings for the various dependencies::

    # TinyMCE settings
    TINYMCE_COMPRESSOR = True
    TINYMCE_DEFAULT_CONFIG = {
        'width': '760',
        'height': '480',
        'plugins': 'fullscreen,media,preview,paste',
        'theme': 'advanced',
        'relative_urls': False,
        'theme_advanced_toolbar_location': 'top',
        'theme_advanced_toolbar_align': 'left',
        'theme_advanced_buttons1': 'bold,italic,underline,strikethrough,|,' \
            'justifyleft,justifycenter,justifyright,justifyfull,|,forecolor,' \
            'formatselect,sub,sup,removeformat,charmap,|,bullist,numlist,|,' \
            'indent,outdent,|,link,unlink,anchor,image,media,|,visualaid,code,' \
            'preview,fullscreen',
        'theme_advanced_buttons2': 'undo,redo,|,cut,copy,paste,pasteword,' \
            'pastetext,selectall,|,cleanup,help,|,hr',
        'theme_advanced_buttons3': '',
        'theme_advanced_blockformats': 'p,pre,address,blockquote,h1,h2,h3,h4,' \
            'h5,h6',
        'plugin_preview_width' : '800',
        'plugin_preview_height' : '600',
        'paste_auto_cleanup_on_paste': 'true',
        }

    # Filebrowser settings
    FILEBROWSER_DIRECTORY = 'uploads/'

    # Grappelli settings
    GRAPPELLI_INDEX_DASHBOARD = \
        'richtext_blog.custom_dashboard.CustomIndexDashboard'

    # richtext_blog settings
    SLUGS_EDITABLE = True
    SITE_DESCRIPTION = 'My blog site'

A full list of TinyMCE configuration options can be found at
http://www.tinymce.com/wiki.php/Configuration
The author spent a little time tweaking TinyMCE to his preferences so feel
free to play around with your own settings. The current settings are fairly
sufficient for most purposes however.

Next you need to edit ``myblogsite/urls.py``. Add the includes::

    from filebrowser.sites import site
    from django.conf import settings

Make sure admin is implemented::

    from django.contrib import admin
    admin.autodiscover()

Next add the url pattern for adding **django-richtext-blog** to the root of the
site::

    url(r'', include('richtext_blog.urls')),  

Add the url pattern for the 3rd party dependencies::

    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^captcha/', include('captcha.urls')),

And the url pattern for the admin pages if not there already::

    url(r'^admin/', include(admin.site.urls)),

For live setups you may need the following pattern so that uploaded images are
viewable::

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),

All rolled up into the one file your ``urls.py`` might look something like::

    from django.conf.urls.defaults import patterns, include, url
    from filebrowser.sites import site
    from django.conf import settings

    # Uncomment the next two lines to enable the admin:
    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = patterns('',
        # richtext_blog definitions
        url(r'', include('richtext_blog.urls')),  
        # 3rd party url definitions
        url(r'^tinymce/', include('tinymce.urls')),
        url(r'^admin/filebrowser/', include(site.urls)),
        url(r'^grappelli/', include('grappelli.urls')),
        url(r'^captcha/', include('captcha.urls')),
        url(r'^admin/', include(admin.site.urls)),

        # Media
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

Save the file, then it's just the matter of preparing the database::

    $ python myblogsite/manage.py syncdb

And if all went well you should be able to run it

    $ python myblogsite/manage.py runserver

Using django-richtext-blog
--------------------------

Creating a new post is all done from the admin pages. Comments can be added and
moderated when viewing a post in the admin section. Author comments can appear
a different colour to public comments on the public side of the site.

The image upload button on TinyMCE when editing a post will open up a the
**django-filebrowser** dialogue where existing uploaded images can be chosen or
new ones uploaded. The image scale can be selected here too.

For syntax highlighting code, the code text must be contained within a
``<pre></pre>`` block. TinyMCE has a shortcut to this in the formatting
drop-down menu listed as *Preformatted*. Pygments will try to guess the code
format but for more accurate control a css class attribute can be provided
that defines the format of the content. For python code simply add a
``class="python"`` to the ``<pre>`` tag in TinyMCE's HTML edit mode so the
opening tag would read ``<pre class="python">``. For simple command line 
formatting use ``class="console"``. For a full list of class names that
can be used, check the list of lexers pygments supports at
http://pygments.org/docs/lexers/ . What is listed under **Short names** is what
should be used as the class name.

A default css stylesheet ``richtext_blog/static/blog-style.css`` is provided 
that implements default styles but can be overidden easily.
http://www.wholebaked.com.au/blog/posts/ is a good example of how custom
styles can change the appearance quite dramatically.

``richtext_blog/templates/base.html`` provides an example of how all the
current features can be rolled up into a site and also shows how to implement
the blog's sidebar features.
