# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-richtext-blog',
    version='1.0.0',
    author=u'Tim Godfrey',
    author_email='http://www.wholebaked.com.au/contact',
    packages=find_packages(),
    install_requires=[
        'django==1.3',
        'django-filebrowser==3.4.2',
        'FeedParser',
        'PIL',
        'django-tinymce==1.5.1b2',
        'MySQL-python',
        'django-autoslug',
        'django-simple-captcha',
        'pygments',
        'BeautifulSoup'
        ]
    url='https://github.com/tum/django-richtext-blog',
    license='BSD licence, see LICENCE.txt',
    description='Simple blogging app that incorporates the use of the rich '
        'text editor, TinyMCE. Supports code syntax highlighting, tags and '
        'comments per post amongst other things',
    long_description=open('README.txt').read(),
    zip_safe=True,
    )
