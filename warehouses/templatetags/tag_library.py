from django import template
from datetime import date
from hydrophore.models import Hydrophore

register = template.Library()

@property
def can_show_button(self):
    return (
        (self.operation_type == "1" and self.situation in ["dismantling", "well_cancellation"]) or
        (self.operation_type == "5" and self.situation in ["installation", "new_well"]) or
        (self.operation_type == "8" and self.situation == "length_extension")
    )

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