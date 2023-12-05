from django import template
import math
from ast import literal_eval

register = template.Library()


@register.filter
def is_nan(value):
    return math.isnan(float(value))

@register.filter
def strip(value):
    return value.replace(' ', '')

@register.filter
def split_colon(value):
    return value.split(';')

@register.filter
def split_comma(value):
    return [i.strip() for i in value.split(',')]

@register.filter
def eval(value):
    return literal_eval(value)


@register.filter
def first_elem(value):
    return value[0]


@register.filter
def replace_slash(value):
    return value.replace('/', '__')