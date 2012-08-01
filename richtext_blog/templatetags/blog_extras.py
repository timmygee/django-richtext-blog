import re
import calendar
import htmlentitydefs

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

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
# Taken from http://effbot.org/zone/re-sub.htm#unescape-html
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

@register.filter
@stringfilter
def pygmentize(value, pre_class=''):
    """
    Expects the raw html content of a post as `value`.
    This function will look through the content for any <pre> tags and update
    their contents to include css classes as per syntax highlighting according
    to pygments.
    Can take an optional argument that dictates what css class the resulting
    'pre' pre tag will have.
    Returns the html passed in with the updated <pre> tags included.
    Loosely based on:
    http://www.ofbrooklyn.com/2010/01/15/syntax-highlighting-django-using-pygments/
    """
    soup = BeautifulSoup(value)
    
    for pre_tag in soup.findAll('pre'):
        # Firstly strip out any markup TinyMCE added to the pre.
        # Typically it will add a <br /> to the end of each line and replace
        # spaces with &nbsp; sequences.
        pre_content_string = ''.join(str(token) for token in pre_tag.contents)
        
        lines = [line.replace('&nbsp;', ' ') \
            for line in pre_content_string.split('<br />')]
        
        pre_content_string = unescape('\n'.join(lines))

        # Check that the tag has a class attribute. If so interpret that as the
        # language of the code contained within the pre tag.
        try:
            pre_tag_class = pre_tag['class']
        except KeyError:
            pre_tag_class = ''
        if pre_tag_class:
            lexer = lexers.get_lexer_by_name(pre_tag_class)
        else:
            # Try and guess the lexer to use
            try:
                lexer = lexers.guess_lexer(pre_content_string)
            except ValueError:
                lexer = lexers.TextLexer()
        highlighted = highlight(
            pre_content_string, lexer, formatters.HtmlFormatter())
        final_soup = BeautifulSoup(highlighted)
        if pre_class:
            for pre_tag in final_soup('pre'):
                pre_tag['class'] = pre_class
        pre_tag.replaceWith(final_soup)
    return mark_safe(soup)
