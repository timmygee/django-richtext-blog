# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup, find_packages

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-richtext-blog',
    version='0.8.3',
    author=u'Tim Godfrey',
    author_email='http://www.wholebaked.com.au/contact',
    include_package_data=True,
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
        ],
    url='https://github.com/tum/django-richtext-blog',
    license='BSD licence, see LICENCE.TXT',
    description='Simple blogging app that incorporates the use of the rich '
        'text editor, TinyMCE. Supports code syntax highlighting, tags and '
        'comments per post with captcha authentication as well as quick image '
        'upload when editing through the use of the filebrowser module.',
    long_description=read('README.RST'),
    zip_safe=False,
)
