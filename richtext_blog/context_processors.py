from datetime import datetime

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from models import Post, Tag
from views import PostListView

def blog_global(request):
    """
    Pass up global context objects
    """
    # Pass up current site object from DB to the template context
    current_site = Site.objects.get_current()
    
    # Create a list of links for the years and months there are blog posts
    # available
    dates = Post.objects.dates('created', 'month')
    now = datetime.now()
    archive_links = []
    seen_years = {}
    for date in dates:
        if date.year < now.year:
            if date.year not in seen_years:
                archive_links.append({
                    'link': reverse('posts_yearly', kwargs={'year': date.year}),
                    'link_text': date.year
                    })
                seen_years[date.year] = None
        else:
            archive_links.append({
                'link': reverse('posts_monthly',
                    kwargs={'year': date.year, 'month': date.strftime('%m')}),
                'link_text': date.strftime('%B %Y')
                })

    # Create a list of tag names, slugs and the number of posts that use the tag
    tag_counts = [{'slug': t.slug, 'count': t.tag_posts.count(), 'name': t.name} \
        for t in Tag.objects.all()]
    
    return {
        'SITE': current_site,
        'ARCHIVE_LINKS': sorted(archive_links, reverse=True),
        'TAG_COUNTS': sorted(tag_counts, key=lambda tag: tag['count'],
            reverse=True)
        }
    
