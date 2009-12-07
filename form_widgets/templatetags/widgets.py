from django import template
from form_widgets.loading import library

register = template.Library()

@register.filter
def as_widget(field, widget_name):
    widget = library.get_widget(widget_name)
    if widget:
        widget = widget()
    return field.as_widget(widget=widget)
