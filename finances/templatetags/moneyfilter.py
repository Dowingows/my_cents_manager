from django import template
from django.utils.formats import number_format

register = template.Library()


@register.filter(name='currency')
def currency(value):
    value = 'R$ {}'.format(
        number_format(value, decimal_pos=2, force_grouping=True)
    )
    return (
        str(value).replace(',', 'temp').replace('.', ',').replace('temp', '.')
    )
