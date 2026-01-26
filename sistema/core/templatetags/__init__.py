from django import template

register = template.Library()

@register.filter
def message_icon(tag):
    """Returns appropriate icon for message tag"""
    icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    }
    return icons.get(tag, 'info-circle')

@register.filter
def add_class(field, css_class):
    """Adds CSS class to form field"""
    return field.as_widget(attrs={"class": css_class})