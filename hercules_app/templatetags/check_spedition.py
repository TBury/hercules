from django import template
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
register = template.Library()

@register.filter(name='file_exists')
def file_exists(path):
    try:
        abs_path = finders.find(path)
        exists = staticfiles_storage.exists(abs_path)
        return exists
    except IOError:
        return False