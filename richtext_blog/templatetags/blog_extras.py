import re
import calendar

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from pygments import lexers, formatters, highlight
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

register = template.Library()

@register.filter
def month_name(value):
    """
    Returns the name of the month for the number passed in. Number must be
    between 1 and 12
    """
    try:
        value = int(value)
    except ValueError:
        return ''
    if value < 1 or value > 12:
        return ''
    return calendar.month_name[value]

@register.filter
@stringfilter
def pygmentize(value, pre_class=''):
    """
    Expects the raw html content of a post as `value`.
    This function will look through the content for any <code> tags and update
    their contents to include css classes as per syntax highlighting according
    to pygments.
    Can take an optional argument that dictates what css class the resulting
    'pre' code tag will have.
    Returns the html passed in with the updated <code> tags included.
    Loosely based on:
    http://www.ofbrooklyn.com/2010/01/15/syntax-highlighting-django-using-pygments/
    """
    soup = BeautifulSoup(value)
    
    for code_tag in soup.findAll('code'):
        # Firstly strip out any markup TinyMCE added to the code.
        # Typically it will add a <br /> to the end of each line. Here we will
        # prettify the contents of the code tag which will bring the <br />
        # tags on to their own line and make the unwanted html bits a little
        # more predictable to find.
        # They can then be removed. As well as this we will replace &nbsp;
        # sequences with spaces.
        keep_lines = []
        for line in code_tag.prettify().splitlines():
            if line.startswith('<br />'):
                continue
            keep_lines.append(line)
        code_tag_string = '\n'.join(keep_lines)
        code_string = BeautifulSoup(code_tag_string,
            convertEntities=BeautifulSoup.HTML_ENTITIES
            ).findAll('code')[0].string
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
        code_soup = BeautifulSoup(highlight(code_string, lexer,
            formatters.HtmlFormatter()))
        if pre_class:
            for pre_tag in code_soup('pre'):
                pre_tag['class'] = pre_class
        code_tag.replaceWith(code_soup)
    return mark_safe(soup)
