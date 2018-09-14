from django import template

register = template.Library()

@register.filter
def parse_details(parse_string):
    parse_string = parse_string.replace('[', '')
    parse_string = parse_string.replace(']', '')
    return parse_string.split(',')