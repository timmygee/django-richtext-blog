from django.contrib.sites.models import Site

def site(request):
    """
    Pass up current site object from DB to the template context
    """
    current_site = Site.objects.get_current()
    return {
        'SITE': current_site,
        }
