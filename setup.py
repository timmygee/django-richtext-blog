# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup, find_packages

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-richtext-blog',
    version='0.8.7',
    author=u'Tim Godfrey',
    author_email='http://www.wholebaked.com.au/contact',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'django==1.11.29',
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
    url='https://github.com/timmygee/django-richtext-blog',
    license='BSD licence, see LICENCE.txt',
    keywords='django blog richtext tinymce',
    description='A django app that implements a blog with the features we\'ve '
        'grown accustomed to. Features: Rich text editing with TinyMCE; Full '
        'image upload support; Tags; Comments; Spam prevention; Atom/RSS '
        'feeds; Example templates; Code syntax highlighting; SEO optimised '
        'urls and more.',
    long_description=read('README.rst'),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary'
        ]
)
