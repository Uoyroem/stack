from django import template

register = template.Library()

@register.filter
def add_class(field, classes):
    return field.as_widget(attrs={"class": classes})
