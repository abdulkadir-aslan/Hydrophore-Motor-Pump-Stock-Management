from django import template
from datetime import date
from hydrophore.models import Hydrophore

register = template.Library()

@register.filter()
def hydrophore_value(value):
    item = Hydrophore.objects.get(id=value)
    return item.serial_number

@register.filter()
def to_start(value):
    return (value-1)*10

@register.filter
def day_diff(value):
    if value:
        return (date.today() - value).days
    return 0