from django import template

register = template.Library()

@register.inclusion_tag('argonemyth_addthis.html')
def addthis(title):
    return {"title": title}
