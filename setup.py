# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup, find_packages

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-richtext-blog',
    version='0.8.4',
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
    description='A django app that implements a blog with the features we''ve '
        'grown accustomed to. Features: Rich text editing with TinyMCE; Full '
        'image upload support; Tags; Comments; Spam prevention; Atom/RSS '
        'feeds; Example templates; Code syntax highlighting; SEO optimised '
        'urls and more.',
    long_description=read('README.RST'),
    zip_safe=False,
)
