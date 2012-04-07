import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from pygments import lexers, formatters, highlight
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

register = template.Library()

@register.filter
@stringfilter
def pygmentize(value):
    """
    Expects the raw html content of a post as `value`.
    This function will look through the content for any <code> tags and update
    their contents to include css classes as per syntax highlighting according
    to pygments.
    It will also use 
    Returns the html passed in with the updated <code> tags included.
    Loosely based on:
    http://www.ofbrooklyn.com/2010/01/15/syntax-highlighting-django-using-pygments/
    """
    soup = BeautifulSoup(value)
    
    for code_tag in soup.findAll('code'):
        # Firstly strip out any markup TinyMCE added to the code.
        # Typically it will add a <br /> to the end of each line and replace
        # spaces with &nbsp; sequences. Here we will prettify the contents of
        # the code tag which will bring the <br /> tags on to their own line
        # and make the unwanted html bits a little more predictable to find.
        # They can then be removed. As well as this we will replace &nbsp;
        # sequences with spaces.
        keep_lines = []
        for line in code_tag.prettify().splitlines():
            if line.startswith('<br />'):
                continue
            keep_lines.append(line.replace('&nbsp;', ' '))
        code_tag_string = '\n'.join(keep_lines)
        code_string = BeautifulSoup(code_tag_string).findAll('code')[0].string
        # Check that the tag has a class attribute. If so interpret that as the
        # language of the code.
        try:
            code_tag_class = code_tag['class']
        except KeyError:
            code_tag_class = ''
        if code_tag_class:
            lexer = lexers.get_lexer_by_name(code_tag_class)
        else:
            # Try and guess the lexer to use
            try:
                lexer = lexers.guess_lexer(code_string)
            except ValueError:
                lexer = lexers.TextLexer()
        code_tag.replaceWith(BeautifulSoup(highlight(code_string, lexer, formatters.HtmlFormatter())))
    return mark_safe(soup)
