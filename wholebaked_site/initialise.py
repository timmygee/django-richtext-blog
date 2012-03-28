#!../venv/bin/python
from django.core.management import setup_environ
from dfm_site import settings

setup_environ(settings)
from django.db import connection, transaction
cursor = connection.cursor()

# Site
from django.contrib.sites.models import Site

site = Site.objects.get(id=1)
site.domain = 'kaihatsu'
site.name = 'Test Site'
site.save()

# Admin user
obj = User.objects.create(
    username='admin', email='tim@wholebaked.com.au',
    is_superuser=True, is_staff=True, first_name='Tim', last_name='Godfrey')
obj.set_password('testing')
obj.save()
