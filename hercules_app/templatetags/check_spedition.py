from django import template
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
register = template.Library()

@register.filter(name='file_exists')
def file_exists(path):
    try:
        abs_path = finders.find(path)
        if staticfiles_storage.exists(abs_path):
            return abs_path
        return "assets/companies/no_company.png"
    except IOError:
        return "assets/companies/no_company.png"