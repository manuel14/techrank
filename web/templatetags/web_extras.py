from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter(name='has_group')
def has_group(user, groupname):
    group = Group.objects.get(name=groupname)
    return True if group in user.groups.all() else False
