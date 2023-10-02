from django import template

register = template.Library()

@register.filter_function
def attr(obj, arg1):
    att, value = arg1.split("=")
    obj.field.widget.attrs[att] = value
    return obj

# @register.filter_function
# def attr(obj, arg1, arg2):
#     att, value = arg1.split("=")
#     att, value = arg2.split("=")
#     obj.field.widget.attrs[att] = value
#     return obj

