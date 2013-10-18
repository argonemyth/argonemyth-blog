from django import template
from django.template.defaultfilters import stringfilter

from pygments import lexers, highlight, formatters
from bs4 import BeautifulSoup


register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def pygmentize(value):
    """
    A filter to highlight code blocks in html with Pygments and BeautifulSoup.

        {% load pygmentize %}

        {{ var_with_code|pygmentize|safe }}

    If you want the code to be highligted for, you have to to put 'class'
    in the <pre> elements. The pre-formatted block will turn to a <code> block.
    """
    soup = BeautifulSoup(unicode(value))
    for block in soup.findAll('pre'):
        #Process HTML -> Replace whitespaces
        #code = block.renderContents().replace('<br />', "\n").replace('&nbsp;', ' ').replace('&gt;', '>') 
        if block.has_key("class"):
            try:
                code = ''.join([unicode(item) for item in block.contents])
                lexer = lexers.get_lexer_by_name(block['class'][0])
                #block.replaceWith(highlight(code, lexer, HtmlFormatter(cssclass="monokai")))
                #formatter = formatters.HtmlFormatter(cssclass="monokai")
                formatter = formatters.HtmlFormatter(linenos=True, cssclass="monokai")
                #formatter = formatters.HtmlFormatter()
                code_hl = highlight(code, lexer, formatter)
                block.contents = [BeautifulSoup(code_hl)]
                block.name = 'code'
            except:
                raise
    return unicode(soup)
