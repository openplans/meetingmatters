from django import template
from meetings import models
from templatetag_sugar.register import tag
from templatetag_sugar.parser import Name, Variable, Constant, Optional, Model

register = template.Library()

@tag(register, [Constant('as'), Name()])
def get_cached_tags(context, asvar):
    tags = models.MeetingTopic.objects.cached()
    context[asvar] = tags
    return ''
