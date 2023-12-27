# finances/templatetags/bootstrap_filters.py
from django import template
from django.forms.fields import ChoiceField
from django.utils.html import format_html

register = template.Library()


@register.filter(name='bootstrap')
def bootstrap(form):
    output = ''
    for field in form:
        widget_class = 'form-control'  # Classe padrão para campos de entrada

        if isinstance(
            field.field, ChoiceField
        ):  # Verifica se é um campo de seleção
            widget_class = 'form-select'  # Adiciona classe específica para campos de seleção

        output += format_html(
            '<div class="form-group">' '   {0} {1}' '   {2}' '</div>',
            field.label_tag(),
            field.as_widget(attrs={'class': widget_class}),
            format_html(
                '<small class="form-text text-muted">{0}</small>',
                field.help_text,
            )
            if field.help_text
            else '',
        )
        if field.errors:
            output += format_html(
                '<div class="text-danger">{0}</div>', ' '.join(field.errors)
            )

    return format_html(output)
