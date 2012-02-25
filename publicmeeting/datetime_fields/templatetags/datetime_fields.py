from django import template
from django import forms

register = template.Library()

@register.filter
def is_datefield(field):
    return isinstance(field.field, forms.DateField)

@register.filter
def is_timefield(field):
    return isinstance(field.field, forms.TimeField)
