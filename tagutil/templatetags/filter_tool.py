# -*- coding: utf-8 -*- 
from django import template
from django.utils.encoding import force_unicode
from linkusall.util import truncatewords,truncatewords_html


register = template.Library()

@register.filter(name='cutwords')
def cutwords(value,arg):
    try:
        length = int(arg)
    except ValueError: # Invalid literal for int().
        return value # Fail silently.
    return truncatewords(value, length)


@register.filter(name='cutwords_html')
def cutwords_html(value,arg):
    try:
        length = int(arg)
    except ValueError: # invalid literal for int()
        return value # Fail silently.
    return truncatewords_html(value, length)


