from django import template

register = template.Library()

@register.filter
def get_first_letter_user(instance):
    # print(instance.username[0])
    return instance.username[0]


@register.filter(name='empty_to_dash')
def empty_to_dash(value):
    if value is None or value == "":
        return "-"
    return value